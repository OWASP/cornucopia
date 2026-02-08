defmodule Copi.RateLimiter do
  @moduledoc """
  GenServer for tracking IP-based rate limits to protect against CAPEC-212 (Functionality Misuse) attacks.

  Maintains separate rate limits for different operations:
  - Game creation
  - Player creation
  - WebSocket connections

  Rate limits are configured via environment variables and automatically clean up expired entries.
  """
  use GenServer
  require Logger

  # Client API

  @doc """
  Starts the RateLimiter GenServer.
  """
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Checks if an IP address has exceeded the rate limit for a given action.

  Returns {:ok, remaining} if under limit, {:error, :rate_limit_exceeded} if over.

  ## Parameters
    - ip: IP address as a tuple (e.g., {127, 0, 0, 1}) or string
    - action: atom representing the action (:game_creation, :player_creation, :connection)

  ## Examples
      iex> Copi.RateLimiter.check_rate("127.0.0.1", :game_creation)
      {:ok, 9}

      iex> Copi.RateLimiter.check_rate({127, 0, 0, 1}, :connection)
      {:error, :rate_limit_exceeded}
  """
  def check_rate(ip, action) when action in [:game_creation, :player_creation, :connection] do
    GenServer.call(__MODULE__, {:check_rate, normalize_ip(ip), action})
  end

  @doc """
  Clears all rate limit data for a specific IP address (useful for testing).
  """
  def clear_ip(ip) do
    GenServer.cast(__MODULE__, {:clear_ip, normalize_ip(ip)})
  end

  @doc """
  Gets the current configuration for rate limits.
  """
  def get_config do
    GenServer.call(__MODULE__, :get_config)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    # Schedule periodic cleanup every 5 minutes
    schedule_cleanup()

    state = %{
      limits: %{
        game_creation: get_env_config(:game_creation_limit, 10),
        player_creation: get_env_config(:player_creation_limit, 20),
        connection: get_env_config(:connection_limit, 50)
      },
      windows: %{
        game_creation: get_env_config(:game_creation_window, 3600),
        player_creation: get_env_config(:player_creation_window, 3600),
        connection: get_env_config(:connection_window, 300)
      },
      requests: %{}
    }

    Logger.info("RateLimiter started with config: #{inspect(state.limits)}")
    {:ok, state}
  end

  @impl true
  def handle_call({:check_rate, ip, action}, _from, state) do
    # Use monotonic time for interval calculations to avoid issues when the system clock changes.
    # V15.4: Safe concurrency and time-of-check correctness.
    now = System.monotonic_time(:millisecond)
    window = state.windows[action]
    limit = state.limits[action]

    key = {ip, action}
    timestamps = Map.get(state.requests, key, [])

    # Convert window (seconds) to the same unit as `now` (milliseconds) for safe comparison.
    window_ms = window * 1_000

    # Remove expired timestamps
    valid_timestamps = Enum.filter(timestamps, fn ts -> now - ts < window_ms end)

    if length(valid_timestamps) >= limit do
      {:reply, {:error, :rate_limit_exceeded}, state}
    else
      new_timestamps = [now | valid_timestamps]
      new_requests = Map.put(state.requests, key, new_timestamps)
      remaining = limit - length(new_timestamps)

      {:reply, {:ok, remaining}, %{state | requests: new_requests}}
    end
  end

  @impl true
  def handle_call(:get_config, _from, state) do
    config = %{
      limits: state.limits,
      windows: state.windows
    }
    {:reply, config, state}
  end

  @impl true
  def handle_cast({:clear_ip, ip}, state) do
    new_requests =
      state.requests
      |> Enum.reject(fn {{request_ip, _action}, _timestamps} -> request_ip == ip end)
      |> Enum.into(%{})

    {:noreply, %{state | requests: new_requests}}
  end

  @impl true
  def handle_info(:cleanup, state) do
    now = System.system_time(:second)

    new_requests =
      state.requests
      |> Enum.map(fn {{ip, action}, timestamps} ->
        window = state.windows[action]
        valid_timestamps = Enum.filter(timestamps, fn ts -> now - ts < window end)
        {{ip, action}, valid_timestamps}
      end)
      |> Enum.reject(fn {_key, timestamps} -> Enum.empty?(timestamps) end)
      |> Enum.into(%{})

    schedule_cleanup()
    {:noreply, %{state | requests: new_requests}}
  end

  # Private helpers

  defp normalize_ip(ip) when is_binary(ip) do
    case :inet.parse_address(String.to_charlist(ip)) do
      {:ok, ip_tuple} -> ip_tuple
      {:error, _} -> ip
    end
  end

  defp normalize_ip(ip) when is_tuple(ip), do: ip
  defp normalize_ip(ip), do: ip

  defp schedule_cleanup do
    Process.send_after(self(), :cleanup, :timer.minutes(5))
  end

  defp get_env_config(key, default) do
    env_var = key |> Atom.to_string() |> String.upcase()

    case System.get_env("RATE_LIMIT_#{env_var}") do
      nil -> default
      value -> String.to_integer(value)
    end
  end
end
