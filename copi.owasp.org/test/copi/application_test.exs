defmodule Copi.ApplicationTest do
  use ExUnit.Case, async: false

  test "RateLimiter is started in supervision tree" do
    # Verify RateLimiter process is running
    assert Process.whereis(Copi.RateLimiter) != nil
  end

  test "RateLimiter responds to configuration requests" do
    config = Copi.RateLimiter.get_config()
    
    assert is_map(config)
    assert Map.has_key?(config, :limits)
    assert Map.has_key?(config, :windows)
  end

  test "application starts successfully" do
    # The application should already be running in tests
    assert Application.started_applications()
           |> Enum.any?(fn {app, _, _} -> app == :copi end)
  end
end
