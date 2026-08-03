defmodule Copi.SessionCleanupTest do
  use ExUnit.Case, async: false

  alias Copi.SessionCleanup

  test "start_link starts and exits cleanly when postgres session storage is disabled" do
    previous = Application.get_env(:copi, :postgres_session_store_enabled)

    on_exit(fn ->
      if is_nil(previous) do
        Application.delete_env(:copi, :postgres_session_store_enabled)
      else
        Application.put_env(:copi, :postgres_session_store_enabled, previous)
      end
    end)

    Application.put_env(:copi, :postgres_session_store_enabled, false)

    assert {:ok, pid} = SessionCleanup.start_link([])
    ref = Process.monitor(pid)
    assert_receive {:DOWN, ^ref, :process, ^pid, :normal}
  end
end
