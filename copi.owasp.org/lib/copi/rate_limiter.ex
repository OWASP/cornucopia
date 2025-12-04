defmodule Copi.RateLimiter do
  @moduledoc """
  Rate limiter to prevent abuse by limiting requests per IP address.
  
  This module implements rate limiting for game creation and user connections
  to protect against CAPEC 212 (Functionality Misuse) attacks.
  """

  use GenServer
  require Logger

  @cleanup_interval :timer.minutes(5)

  # Client API

  @doc """
  Starts the rate limiter GenServer.
  """
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @doc """
  Checks if a request from the given IP for the specified action should be allowed.
  
  Returns `{:ok, remaining}` if allowed, `{:error, :rate_limited, retry_after}` if blocked.
  """
  def check_rate(ip_address, action) when action in [:game_creation, :connection] do
    GenServer.call(__MODULE__, {:check_rate, ip_address, action})
  end

  @doc """
  Records a successful action for rate limiting tracking.
  """
  def record_action(ip_address, action) when action in [:game_creation, :connection] do
    GenServer.cast(__MODULE__, {:record_action, ip_address, action})
  end

  @doc """
  Clears all rate limit data for an IP address (useful for testing).
  """
  def clear_ip(ip_address) do
    GenServer.cast(__MODULE__, {:clear_ip, ip_address})
  end

  @doc """
  Gets current rate limit configuration.
  """
  def get_config do
    GenServer.call(__MODULE__, :get_config)
  end

  # Server callbacks

  @impl true
  def init(_opts) do
    # Schedule periodic cleanup
    schedule_cleanup()

    config = %{
      game_creation: %{
        max_requests: get_env(:max_games_per_ip, 10),
        window_seconds: get_env(:game_creation_window_seconds, 3600)
      },
      connection: %{
        max_requests: get_env(:max_connections_per_ip, 50),
        window_seconds: get_env(:connection_window_seconds, 300)
      }
    }

    state = %{
      requests: %{},
      config: config
    }

    Logger.info("RateLimiter started with config: #{inspect(config)}")

    {:ok, state}
  end

  @impl true
  def handle_call({:check_rate, ip_address, action}, _from, state) do
    now = System.system_time(:second)
    config = state.config[action]
    
    ip_requests = get_ip_requests(state, ip_address, action)
    
    # Filter out expired requests
    valid_requests = Enum.filter(ip_requests, fn timestamp ->
      now - timestamp < config.window_seconds
    end)

    count = length(valid_requests)
    remaining = max(0, config.max_requests - count)

    if count < config.max_requests do
      {:reply, {:ok, remaining}, state}
    else
      oldest_request = List.first(valid_requests)
      retry_after = oldest_request + config.window_seconds - now
      
      Logger.warning(
        "Rate limit exceeded for IP #{inspect(ip_address)}, action: #{action}, " <>
        "count: #{count}/#{config.max_requests}, retry_after: #{retry_after}s"
      )
      
      {:reply, {:error, :rate_limited, retry_after}, state}
    end
  end

  @impl true
  def handle_call(:get_config, _from, state) do
    {:reply, state.config, state}
  end

  @impl true
  def handle_cast({:record_action, ip_address, action}, state) do
    now = System.system_time(:second)
    
    ip_requests = get_ip_requests(state, ip_address, action)
    updated_requests = [now | ip_requests]
    
    new_requests = put_in(
      state.requests,
      [ip_address, action],
      updated_requests
    )

    {:noreply, %{state | requests: new_requests}}
  end

  @impl true
  def handle_cast({:clear_ip, ip_address}, state) do
    new_requests = Map.delete(state.requests, ip_address)
    {:noreply, %{state | requests: new_requests}}
  end

  @impl true
  def handle_info(:cleanup, state) do
    now = System.system_time(:second)
    
    cleaned_requests = state.requests
    |> Enum.map(fn {ip, actions} ->
      cleaned_actions = actions
      |> Enum.map(fn {action, timestamps} ->
        config = state.config[action]
        valid_timestamps = Enum.filter(timestamps, fn timestamp ->
          now - timestamp < config.window_seconds
        end)
        {action, valid_timestamps}
      end)
      |> Enum.filter(fn {_action, timestamps} -> length(timestamps) > 0 end)
      |> Map.new()
      
      {ip, cleaned_actions}
    end)
    |> Enum.filter(fn {_ip, actions} -> map_size(actions) > 0 end)
    |> Map.new()

    schedule_cleanup()
    
    {:noreply, %{state | requests: cleaned_requests}}
  end

  # Private helpers

  defp get_ip_requests(state, ip_address, action) do
    get_in(state.requests, [ip_address, action]) || []
  end

  defp schedule_cleanup do
    Process.send_after(self(), :cleanup, @cleanup_interval)
  end

  defp get_env(key, default) do
    Application.get_env(:copi, __MODULE__, [])
    |> Keyword.get(key, default)
  end
end
