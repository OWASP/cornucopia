defmodule CopiWeb.TelemetryTest do
  use ExUnit.Case, async: true

  test "telemetry supervisor starts successfully" do
    assert Process.whereis(CopiWeb.Telemetry) != nil
  end

  test "metrics/0 returns telemetry metrics" do
    metrics = CopiWeb.Telemetry.metrics()
    
    assert is_list(metrics)
    assert length(metrics) > 0
    
    # Check that we have Phoenix metrics
    assert Enum.any?(metrics, fn metric ->
      metric.name == [:phoenix, :endpoint, :stop, :duration]
    end)
    
    # Check that we have database metrics
    assert Enum.any?(metrics, fn metric ->
      metric.name == [:copi, :repo, :query, :total_time]
    end)
    
    # Check that we have VM metrics
    assert Enum.any?(metrics, fn metric ->
      metric.name == [:vm, :memory, :total]
    end)
  end
end
