defmodule Copi.ApplicationTest do
  use ExUnit.Case
  test "application supervisor is running" do
    assert Process.whereis(Copi.Supervisor) != nil
  end
  test "config_change returns ok" do
    assert :ok == Copi.Application.config_change([], [], [])
  end
  test "application starts successfully" do
    # The application should already be running in tests
    assert Application.started_applications()
           |> Enum.any?(fn {app, _, _} -> app == :copi end)
  end
  test "config_change handles updates successfully" do
    # This evaluates the application config update hook natively.
    assert :ok = Copi.Application.config_change([foo: :bar], [foo: :baz], [])
  end
end