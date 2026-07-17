defmodule Copi.PlayerCapabilityRegistryTest do
  use ExUnit.Case, async: false

  alias Copi.PlayerCapabilityRegistry

  setup do
    :sys.replace_state(PlayerCapabilityRegistry, fn state ->
      %{state | consumed: %{}}
    end)

    :ok
  end

  test "consumes a capability only once" do
    capability = "one-time-capability"

    assert :ok = PlayerCapabilityRegistry.consume(capability)
    assert {:error, :already_used} = PlayerCapabilityRegistry.consume(capability)
  end

  test "stores a digest instead of the capability" do
    capability = "sensitive-capability"

    assert :ok = PlayerCapabilityRegistry.consume(capability)

    state = :sys.get_state(PlayerCapabilityRegistry)
    refute Map.has_key?(state.consumed, capability)
    assert Map.has_key?(state.consumed, :crypto.hash(:sha256, capability))
  end

  test "allows exactly one concurrent consumer" do
    capability = "concurrent-capability"

    results =
      1..10
      |> Enum.map(fn _ -> Task.async(fn -> PlayerCapabilityRegistry.consume(capability) end) end)
      |> Task.await_many()

    assert Enum.count(results, &(&1 == :ok)) == 1
    assert Enum.count(results, &(&1 == {:error, :already_used})) == 9
  end

  test "removes expired digests before consuming" do
    capability = "expired-registry-entry"
    digest = :crypto.hash(:sha256, capability)

    :sys.replace_state(PlayerCapabilityRegistry, fn state ->
      %{state | consumed: %{digest => System.system_time(:millisecond) - 1}}
    end)

    assert :ok = PlayerCapabilityRegistry.consume(capability)
  end

  test "uses local replay protection by default" do
    state = :sys.get_state(PlayerCapabilityRegistry)

    refute state.cluster_enabled
    assert :undefined == :global.whereis_name(state.global_name)
  end

  test "cluster mode merges active entries before accepting a capability" do
    name = :cluster_registry_test
    global_name = {:cluster_registry_test, System.unique_integer([:positive])}
    capability = "capability-consumed-on-another-node"
    digest = :crypto.hash(:sha256, capability)
    expires_at = System.system_time(:millisecond) + :timer.minutes(5)

    start_supervised!(
      {PlayerCapabilityRegistry, name: name, cluster_enabled: true, global_name: global_name}
    )

    assert %{^digest => ^expires_at} =
             GenServer.call(name, {:merge_consumed, %{digest => expires_at}})

    assert {:error, :already_used} = PlayerCapabilityRegistry.consume(name, capability)
    send(name, :cluster_sync)
    assert eventually(fn -> is_pid(:global.whereis_name(global_name)) end)
  end

  test "cluster mode falls back to local replay protection when the global owner is unavailable" do
    name = :cluster_fallback_registry_test
    global_name = {:cluster_fallback_registry_test, System.unique_integer([:positive])}
    unavailable_owner = spawn(fn -> Process.sleep(:infinity) end)
    :yes = :global.register_name(global_name, unavailable_owner)

    start_supervised!(
      {PlayerCapabilityRegistry, name: name, cluster_enabled: true, global_name: global_name}
    )

    assert :ok = PlayerCapabilityRegistry.consume(name, "fallback-capability")

    assert {:error, :already_used} =
             PlayerCapabilityRegistry.consume(name, "fallback-capability")

    Process.exit(unavailable_owner, :kill)
  end

  test "cluster mode synchronizes a locally consumed digest with the global owner" do
    owner_name = :cluster_owner_registry_test
    follower_name = :cluster_follower_registry_test
    global_name = {:cluster_sync_registry_test, System.unique_integer([:positive])}
    capability = "locally-consumed-during-partition"
    digest = :crypto.hash(:sha256, capability)
    expires_at = System.system_time(:millisecond) + :timer.minutes(5)

    start_supervised!(
      Supervisor.child_spec(
        {PlayerCapabilityRegistry,
         name: owner_name, cluster_enabled: true, global_name: global_name},
        id: owner_name
      )
    )

    send(owner_name, :cluster_sync)
    assert eventually(fn -> :global.whereis_name(global_name) == Process.whereis(owner_name) end)

    start_supervised!(
      Supervisor.child_spec(
        {PlayerCapabilityRegistry,
         name: follower_name, cluster_enabled: true, global_name: global_name},
        id: follower_name
      )
    )

    GenServer.call(follower_name, {:merge_consumed, %{digest => expires_at}})
    send(follower_name, :cluster_sync)

    assert eventually(fn ->
             match?(
               {:error, :already_used},
               PlayerCapabilityRegistry.consume(owner_name, capability)
             )
           end)
  end

  defp eventually(check, attempts \\ 20)

  defp eventually(check, attempts) when attempts > 0 do
    if check.() do
      true
    else
      Process.sleep(10)
      eventually(check, attempts - 1)
    end
  end

  defp eventually(_check, 0), do: false
end
