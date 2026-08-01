defmodule Copi.PlayerCapabilityRegistry do
  @moduledoc false

  use GenServer

  import Ecto.Query

  alias Copi.PlayerCapabilityConsumption
  alias Copi.Repo

  @retention_ms :timer.minutes(5)
  @cleanup_interval_ms :timer.minutes(1)
  @sync_interval_ms :timer.seconds(1)
  @cluster_call_timeout_ms 1_000
  @default_global_name {__MODULE__, :cluster}

  def start_link(opts \\ []) do
    name = Keyword.get(opts, :name, __MODULE__)
    GenServer.start_link(__MODULE__, opts, name: name)
  end

  def consume(capability) when is_binary(capability) do
    consume(__MODULE__, capability)
  end

  def consume(server, capability) when is_binary(capability) do
    digest = :crypto.hash(:sha256, capability)
    expires_at = System.system_time(:millisecond) + @retention_ms

    if postgres_enabled?() do
      consume_in_postgres(digest, expires_at)
    else
      GenServer.call(server, {:consume, digest, expires_at})
    end
  end

  @impl true
  def init(opts) do
    cluster_enabled =
      Keyword.get(
        opts,
        :cluster_enabled,
        Application.get_env(:copi, :player_capability_cluster_enabled, false)
      ) and not postgres_enabled?()

    state = %{
      consumed: %{},
      cluster_enabled: cluster_enabled,
      global_name: Keyword.get(opts, :global_name, @default_global_name)
    }

    schedule_cleanup()

    if cluster_enabled do
      :net_kernel.monitor_nodes(true, node_type: :visible)
      schedule_sync(0)
    end

    {:ok, state}
  end

  @impl true
  def handle_call({:consume, digest, expires_at}, _from, state) do
    now = System.system_time(:millisecond)
    state = remove_expired(state, now)

    case consume_with_mode(state, digest, expires_at) do
      {result, updated_state} -> {:reply, result, updated_state}
    end
  end

  def handle_call({:consume_cluster, digest, expires_at}, _from, state) do
    now = System.system_time(:millisecond)
    state = remove_expired(state, now)
    {result, updated_state} = consume_locally(state, digest, expires_at)
    existing_expiry = Map.get(updated_state.consumed, digest)

    {:reply, {result, existing_expiry}, updated_state}
  end

  def handle_call({:merge_consumed, incoming}, _from, state) when is_map(incoming) do
    now = System.system_time(:millisecond)
    state = remove_expired(state, now)
    merged = merge_active(state.consumed, incoming, now)

    {:reply, merged, %{state | consumed: merged}}
  end

  @impl true
  def handle_info(:cluster_sync, %{cluster_enabled: true} = state) do
    state = sync_with_cluster(state)
    schedule_sync(@sync_interval_ms)
    {:noreply, state}
  end

  def handle_info({:nodeup, _node, _info}, %{cluster_enabled: true} = state) do
    schedule_sync(0)
    {:noreply, state}
  end

  def handle_info({:nodedown, _node, _info}, state), do: {:noreply, state}

  @impl true
  def handle_info(:cleanup, state) do
    schedule_cleanup()
    {:noreply, remove_expired(state, System.system_time(:millisecond))}
  end

  defp consume_with_mode(%{cluster_enabled: false} = state, digest, expires_at) do
    consume_locally(state, digest, expires_at)
  end

  defp consume_with_mode(%{cluster_enabled: true} = state, digest, expires_at) do
    if Map.has_key?(state.consumed, digest) do
      {{:error, :already_used}, state}
    else
      {owner, state} = global_owner(state)

      cond do
        owner == self() ->
          consume_locally(state, digest, expires_at)

        is_pid(owner) ->
          case call_cluster(owner, {:consume_cluster, digest, expires_at}) do
            {:ok, {result, cluster_expiry}} ->
              consumed = Map.put(state.consumed, digest, cluster_expiry)
              {result, %{state | consumed: consumed}}

            :unavailable ->
              consume_locally(state, digest, expires_at)
          end

        true ->
          consume_locally(state, digest, expires_at)
      end
    end
  end

  defp consume_locally(state, digest, expires_at) do
    if Map.has_key?(state.consumed, digest) do
      {{:error, :already_used}, state}
    else
      {:ok, %{state | consumed: Map.put(state.consumed, digest, expires_at)}}
    end
  end

  defp sync_with_cluster(state) do
    now = System.system_time(:millisecond)
    state = remove_expired(state, now)
    {owner, state} = global_owner(state)

    cond do
      owner == self() ->
        state

      is_pid(owner) ->
        case call_cluster(owner, {:merge_consumed, state.consumed}) do
          {:ok, merged} -> %{state | consumed: merge_active(state.consumed, merged, now)}
          :unavailable -> state
        end

      true ->
        state
    end
  end

  defp global_owner(state) do
    case :global.whereis_name(state.global_name) do
      :undefined ->
        case :global.register_name(state.global_name, self()) do
          :yes -> {self(), state}
          :no -> {:global.whereis_name(state.global_name), state}
        end

      owner ->
        {owner, state}
    end
  end

  defp call_cluster(owner, message) do
    try do
      {:ok, GenServer.call(owner, message, @cluster_call_timeout_ms)}
    catch
      :exit, _reason -> :unavailable
    end
  end

  defp merge_active(left, right, now) do
    left
    |> Map.merge(right, fn _digest, left_expiry, right_expiry ->
      max(left_expiry, right_expiry)
    end)
    |> Map.reject(fn {_digest, expires_at} -> expires_at <= now end)
  end

  defp remove_expired(state, now) do
    %{
      state
      | consumed: Map.reject(state.consumed, fn {_digest, expires_at} -> expires_at <= now end)
    }
  end

  defp schedule_cleanup do
    Process.send_after(self(), :cleanup, @cleanup_interval_ms)
  end

  defp schedule_sync(delay) do
    Process.send_after(self(), :cluster_sync, delay)
  end

  defp consume_in_postgres(digest, expires_at_ms) do
    now = DateTime.utc_now()
    expires_at = DateTime.from_unix!(expires_at_ms * 1_000, :microsecond)

    Repo.delete_all(
      from consumption in PlayerCapabilityConsumption,
        where: consumption.expires_at <= ^now
    )

    case Repo.insert_all(
           PlayerCapabilityConsumption,
           [%{digest: digest, expires_at: expires_at}],
           on_conflict: :nothing,
           conflict_target: [:digest]
         ) do
      {1, _} -> :ok
      {0, _} -> {:error, :already_used}
    end
  end

  defp postgres_enabled? do
    Application.get_env(:copi, :postgres_session_store_enabled, false)
  end
end
