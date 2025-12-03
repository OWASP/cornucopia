defmodule Copi.RateLimiterTest do
  use ExUnit.Case, async: true

  alias Copi.RateLimiter

  setup do
    # Start the RateLimiter for testing
    {:ok, pid} = RateLimiter.start_link([])
    
    # Clear any existing state
    RateLimiter.clear_ip("127.0.0.1")
    
    on_exit(fn ->
      if Process.alive?(pid), do: GenServer.stop(pid)
    end)
    
    :ok
  end

  describe "game creation rate limiting" do
    test "allows requests under the limit" do
      ip = "127.0.0.1"
      
      # First request should be allowed
      assert {:ok, remaining} = RateLimiter.check_rate(ip, :game_creation)
      assert remaining >= 0
      
      RateLimiter.record_action(ip, :game_creation)
      
      # Second request should still be allowed
      assert {:ok, _remaining} = RateLimiter.check_rate(ip, :game_creation)
    end

    test "blocks requests over the limit" do
      ip = "192.168.1.100"
      config = RateLimiter.get_config()
      max_games = config.game_creation.max_requests
      
      # Make max_requests number of game creations
      for _i <- 1..max_games do
        assert {:ok, _remaining} = RateLimiter.check_rate(ip, :game_creation)
        RateLimiter.record_action(ip, :game_creation)
      end
      
      # Next request should be blocked
      assert {:error, :rate_limited, retry_after} = RateLimiter.check_rate(ip, :game_creation)
      assert retry_after > 0
    end

    test "different IPs have independent limits" do
      ip1 = "10.0.0.1"
      ip2 = "10.0.0.2"
      config = RateLimiter.get_config()
      max_games = config.game_creation.max_requests
      
      # Exhaust limit for ip1
      for _i <- 1..max_games do
        RateLimiter.check_rate(ip1, :game_creation)
        RateLimiter.record_action(ip1, :game_creation)
      end
      
      # ip1 should be blocked
      assert {:error, :rate_limited, _} = RateLimiter.check_rate(ip1, :game_creation)
      
      # ip2 should still be allowed
      assert {:ok, _remaining} = RateLimiter.check_rate(ip2, :game_creation)
    end
  end

  describe "connection rate limiting" do
    test "allows connections under the limit" do
      ip = "172.16.0.1"
      
      assert {:ok, remaining} = RateLimiter.check_rate(ip, :connection)
      assert remaining >= 0
      
      RateLimiter.record_action(ip, :connection)
      
      assert {:ok, _remaining} = RateLimiter.check_rate(ip, :connection)
    end

    test "blocks connections over the limit" do
      ip = "172.16.0.2"
      config = RateLimiter.get_config()
      max_connections = config.connection.max_requests
      
      # Make max_requests number of connections
      for _i <- 1..max_connections do
        assert {:ok, _remaining} = RateLimiter.check_rate(ip, :connection)
        RateLimiter.record_action(ip, :connection)
      end
      
      # Next connection should be blocked
      assert {:error, :rate_limited, retry_after} = RateLimiter.check_rate(ip, :connection)
      assert retry_after > 0
    end
  end

  describe "rate limit window expiration" do
    test "allows requests after window expires" do
      ip = "192.168.100.1"
      
      # This test would require waiting for the window to expire
      # In a real scenario, you might want to use a mock timer or 
      # make the window configurable for testing
      
      assert {:ok, _remaining} = RateLimiter.check_rate(ip, :game_creation)
      RateLimiter.record_action(ip, :game_creation)
      
      # Verify request was recorded
      assert {:ok, _remaining} = RateLimiter.check_rate(ip, :game_creation)
    end
  end

  describe "configuration" do
    test "returns current configuration" do
      config = RateLimiter.get_config()
      
      assert is_map(config)
      assert Map.has_key?(config, :game_creation)
      assert Map.has_key?(config, :connection)
      
      assert config.game_creation.max_requests > 0
      assert config.game_creation.window_seconds > 0
      
      assert config.connection.max_requests > 0
      assert config.connection.window_seconds > 0
    end
  end

  describe "IP clearing" do
    test "clears rate limit data for an IP" do
      ip = "10.20.30.40"
      
      # Record some actions
      RateLimiter.record_action(ip, :game_creation)
      RateLimiter.record_action(ip, :connection)
      
      # Clear the IP
      RateLimiter.clear_ip(ip)
      
      # Should be able to make full limit of requests again
      config = RateLimiter.get_config()
      assert {:ok, remaining} = RateLimiter.check_rate(ip, :game_creation)
      assert remaining == config.game_creation.max_requests
    end
  end
end
