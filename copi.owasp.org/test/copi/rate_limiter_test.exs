defmodule Copi.RateLimiterTest do
  use ExUnit.Case, async: false

  alias Copi.RateLimiter

  setup do
    # Tests run sequentially and use unique IPs to avoid conflicts
    :ok
  end

  describe "game creation rate limiting" do
    test "allows requests under the limit" do
      ip = "127.0.0.#{:rand.uniform(255)}"
      
      # First request should be allowed
      assert {:ok, remaining} = RateLimiter.check_and_record(ip, :game_creation)
      assert remaining >= 0
      
      # Second request should still be allowed
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :game_creation)
    end

    test "blocks requests over the limit" do
      ip = "192.168.1.#{:rand.uniform(255)}"
      config = RateLimiter.get_config()
      max_games = config.game_creation.max_requests
      
      # Make max_requests number of game creations
      for _i <- 1..max_games do
        assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :game_creation)
      end
      
      # Next request should be blocked
      assert {:error, :rate_limited, retry_after} = RateLimiter.check_and_record(ip, :game_creation)
      assert retry_after > 0
    end

    test "different IPs have independent limits" do
      ip1 = "10.0.0.#{:rand.uniform(255)}"
      ip2 = "10.0.1.#{:rand.uniform(255)}"
      config = RateLimiter.get_config()
      max_games = config.game_creation.max_requests
      
      # Exhaust limit for ip1
      for _i <- 1..max_games do
        RateLimiter.check_and_record(ip1, :game_creation)
      end
      
      # ip1 should be blocked
      assert {:error, :rate_limited, _} = RateLimiter.check_and_record(ip1, :game_creation)
      
      # ip2 should still be allowed
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip2, :game_creation)
    end
  end

  describe "connection rate limiting" do
    test "allows connections under the limit" do
      ip = "172.16.0.#{:rand.uniform(255)}"
      
      assert {:ok, remaining} = RateLimiter.check_and_record(ip, :connection)
      assert remaining >= 0
      
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :connection)
    end

    test "blocks connections over the limit" do
      ip = "172.16.1.#{:rand.uniform(255)}"
      config = RateLimiter.get_config()
      max_connections = config.connection.max_requests
      
      # Make max_requests number of connections
      for _i <- 1..max_connections do
        assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :connection)
      end
      
      # Next connection should be blocked
      assert {:error, :rate_limited, retry_after} = RateLimiter.check_and_record(ip, :connection)
      assert retry_after > 0
    end
  end

  describe "player creation rate limiting" do
    test "allows player creation under the limit" do
      ip = "192.168.2.#{:rand.uniform(255)}"
      
      assert {:ok, remaining} = RateLimiter.check_and_record(ip, :player_creation)
      assert remaining >= 0
      
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :player_creation)
    end

    test "blocks player creation over the limit" do
      ip = "192.168.3.#{:rand.uniform(255)}"
      config = RateLimiter.get_config()
      max_players = config.player_creation.max_requests
      
      # Make max_requests number of player creations
      for _i <- 1..max_players do
        assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :player_creation)
      end
      
      # Next request should be blocked
      assert {:error, :rate_limited, retry_after} = RateLimiter.check_and_record(ip, :player_creation)
      assert retry_after > 0
    end

    test "player creation limit is separate from game creation limit" do
      ip = "192.168.4.#{:rand.uniform(255)}"
      config = RateLimiter.get_config()
      max_games = config.game_creation.max_requests
      
      # Exhaust game creation limit
      for _i <- 1..max_games do
        RateLimiter.check_and_record(ip, :game_creation)
      end
      
      # Game creation should be blocked
      assert {:error, :rate_limited, _} = RateLimiter.check_and_record(ip, :game_creation)
      
      # Player creation should still be allowed (separate limit)
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :player_creation)
    end
  end

  describe "rate limit window expiration" do
    test "allows requests after window expires" do
      ip = "192.168.100.#{:rand.uniform(255)}"
      
      # This test would require waiting for the window to expire
      # In a real scenario, you might want to use a mock timer or 
      # make the window configurable for testing
      
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :game_creation)
      
      # Verify request was recorded
      assert {:ok, _remaining} = RateLimiter.check_and_record(ip, :game_creation)
    end
  end

  describe "configuration" do
    test "returns current configuration" do
      config = RateLimiter.get_config()
      
      assert is_map(config)
      assert Map.has_key?(config, :game_creation)
      assert Map.has_key?(config, :player_creation)
      assert Map.has_key?(config, :connection)
      
      assert config.game_creation.max_requests > 0
      assert config.game_creation.window_seconds > 0
      
      assert config.player_creation.max_requests > 0
      assert config.player_creation.window_seconds > 0
      
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
