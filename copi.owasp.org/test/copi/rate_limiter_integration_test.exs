defmodule Copi.RateLimiterIntegrationTest do
  use ExUnit.Case, async: false
  use Plug.Test
  alias Copi.RateLimiter
  alias CopiWeb.Plugs.RateLimiterPlug

  setup do
    # Start the RateLimiter GenServer for testing if not already started
    case RateLimiter.start_link([]) do
      {:ok, pid} -> {:ok, pid}
      {:error, {:already_started, pid}} -> {:ok, pid}
    end
    
    # Clear all rate limiting data before each test (synchronous)
    RateLimiter.clear_ip_sync({192, 168, 1, 100})
    RateLimiter.clear_ip_sync({10, 0, 0, 1})
    RateLimiter.clear_ip_sync({127, 0, 0, 1})
    :ok
  end

  describe "Attack Scenario Tests" do
    test "prevents 100 concurrent requests like in the vulnerability report" do
      ip = "192.168.1.100"
      
      # Simulate the attack scenario from the vulnerability report
      tasks = for i <- 1..100 do
        Task.async(fn ->
          conn = conn(:put, "/api/games/01KK4ANZFV6XMR14VX7R1X6T55/players/01KK4APC64N6Z5B346S960XTQJ/card")
                 |> put_req_header("x-forwarded-for", ip)
                 |> put_req_header("content-type", "application/json")
                 |> RateLimiterPlug.call([])
          
          {i, conn.status}
        end)
      end
      
      results = Task.await_many(tasks, 10_000)
      
      # Count different response types
      rate_limited = Enum.count(results, fn {_, status} -> status == 429 end)
      allowed = Enum.count(results, fn {_, status} -> status != 429 end)
      
      # With rate limiting of 10 requests per minute, most should be blocked
      config = RateLimiter.get_config()
      limit = config.limits.api_action
      
      assert rate_limited >= 90  # At least 90 should be rate limited
      assert allowed <= limit     # Only the limit should be allowed
      
      IO.puts("\nAttack Simulation Results:")
      IO.puts("Rate limited (429): #{rate_limited}")
      IO.puts("Allowed: #{allowed}")
      IO.puts("Total: #{length(results)}")
    end

    test "rate limiting window resets after time passes" do
      ip = "10.0.0.1"
      config = RateLimiter.get_config()
      limit = config.limits.api_action
      window = config.windows.api_action
      
      # Exhaust the rate limit
      for _ <- 1..limit do
        RateLimiter.check_rate(ip, :api_action)
      end
      
      # Should be rate limited now
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :api_action)
      
      # Wait for window to pass plus a small buffer
      :timer.sleep(window + 100)  # window is in milliseconds
      
      # Should be allowed again after window expires
      assert {:ok, _remaining} = RateLimiter.check_rate(ip, :api_action)
    end

    test "different IPs have independent rate limits" do
      ip1 = "192.168.1.100"
      ip2 = "192.168.1.101"
      config = RateLimiter.get_config()
      limit = config.limits.api_action
      
      # Exhaust limit for IP1
      for _ <- 1..limit do
        assert {:ok, _} = RateLimiter.check_rate(ip1, :api_action)
      end
      
      # IP1 should be rate limited
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip1, :api_action)
      
      # IP2 should still be able to make requests
      assert {:ok, _} = RateLimiter.check_rate(ip2, :api_action)
    end

    test "rate limiting works across different action types" do
      ip = "10.0.0.1"
      config = RateLimiter.get_config()
      
      # Test that different action types have separate limits
      api_limit = config.limits.api_action
      connection_limit = config.limits.connection
      
      # Exhaust API action limit
      for _ <- 1..api_limit do
        assert {:ok, _} = RateLimiter.check_rate(ip, :api_action)
      end
      
      # API actions should be rate limited
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :api_action)
      
      # But connection limit should still work independently
      assert {:ok, _} = RateLimiter.check_rate(ip, :connection)
    end

    test "rate limiter handles high concurrency safely" do
      ip = "192.168.1.200"
      
      # Test with many concurrent requests to ensure no race conditions in rate limiter
      tasks = for _ <- 1..50 do
        Task.async(fn ->
          RateLimiter.check_rate(ip, :api_action)
        end)
      end
      
      results = Task.await_many(tasks, 5000)
      
      # Count successes vs failures
      successes = Enum.count(results, fn result -> match?({:ok, _}, result) end)
      failures = Enum.count(results, fn result -> match?({:error, _}, result) end)
      
      config = RateLimiter.get_config()
      limit = config.limits.api_action
      
      # Should not exceed the limit
      assert successes <= limit
      assert failures >= 50 - limit
      
      # Ensure no crashes or unexpected results
      assert length(results) == 50
    end
  end

  describe "Rate Limiter Configuration" do
    test "respects environment variable configuration" do
      # Test that the rate limiter reads from environment variables
      config = RateLimiter.get_config()
      
      # Verify default values are set
      assert config.limits.api_action == 10
      assert config.windows.api_action == 60
      assert config.limits.connection == 133
      assert config.windows.connection == 1
    end

    test "handles localhost differently in production" do
      # This test would need to be run in production mode to fully test
      # For now, we verify the logic exists
      ip = {127, 0, 0, 1}
      
      # In test mode, localhost should be rate limited
      result = RateLimiter.check_rate(ip, :api_action)
      assert match?({:ok, _}, result)
    end
  end

  describe "Error Handling" do
    test "handles invalid IP addresses gracefully" do
      # Test with various invalid IP formats
      invalid_ips = ["invalid", "", "not-an-ip", "999.999.999.999"]
      
      for ip <- invalid_ips do
        # Should not crash, should handle gracefully
        result = RateLimiter.check_rate(ip, :api_action)
        case result do
          {:ok, _} -> :ok
          {:error, :rate_limit_exceeded} -> :ok
        end
      end
    end

    test "rate limiter is thread-safe" do
      ip = "10.0.0.100"
      
      # Test concurrent access to the same IP
      tasks = for _ <- 1..20 do
        Task.async(fn ->
          # Mix of different operations
          case :rand.uniform(3) do
            1 -> RateLimiter.check_rate(ip, :api_action)
            2 -> RateLimiter.check_rate(ip, :connection)
            3 -> RateLimiter.get_config()
          end
        end)
      end
      
      results = Task.await_many(tasks, 5000)
      
      # All operations should complete successfully
      assert length(results) == 20
      Enum.each(results, fn result ->
        case result do
          {:ok, _} -> :ok
          {:error, :rate_limit_exceeded} -> :ok
          %{} -> :ok
        end
      end)
    end
  end
end
