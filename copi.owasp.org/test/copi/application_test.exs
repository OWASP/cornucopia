defmodule Copi.ApplicationTest do
  use ExUnit.Case

  test "application supervisor is running" do
    assert Process.whereis(Copi.Supervisor) != nil
  end

  test "config_change returns ok" do
    assert :ok == Copi.Application.config_change([], [], [])
  end
end