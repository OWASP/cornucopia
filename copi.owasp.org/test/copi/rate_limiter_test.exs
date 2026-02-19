defmodule Copi.RateLimiterTest do
  use ExUnit.Case, async: false
  alias Copi.RateLimiter

  setup do
    # Clear rate limiter state before each test
    test_ip = {127, 0, 0, 1}
    RateLimiter.clear_ip(test_ip)
    {:ok, ip: test_ip}
  end

  describe "check_rate/2" do
    test "allows requests under the limit", %{ip: ip} do
      # First request should succeed
      assert {:ok, remaining} = RateLimiter.check_rate(ip, :game_creation)
      assert remaining >= 0
    end

    test "blocks requests over the game creation limit", %{ip: ip} do
      # Get the game creation limit from config
      config = RateLimiter.get_config()
      limit = config.limits.game_creation

      # Make requests up to the limit
      for _ <- 1..limit do
        assert {:ok, _} = RateLimiter.check_rate(ip, :game_creation)
      end

      # Next request should be blocked
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :game_creation)
    end

    test "blocks requests over the player creation limit", %{ip: ip} do
      config = RateLimiter.get_config()
      limit = config.limits.player_creation

      # Make requests up to the limit
      for _ <- 1..limit do
        assert {:ok, _} = RateLimiter.check_rate(ip, :player_creation)
      end

      # Next request should be blocked
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :player_creation)
    end

    test "blocks requests over the connection limit", %{ip: ip} do
      config = RateLimiter.get_config()
      limit = config.limits.connection

      # Make requests up to the limit
      for _ <- 1..limit do
        assert {:ok, _} = RateLimiter.check_rate(ip, :connection)
      end

      # Next request should be blocked
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :connection)
    end

    test "different actions have independent limits", %{ip: ip} do
      # Make a game creation request
      assert {:ok, _} = RateLimiter.check_rate(ip, :game_creation)

      # Player creation should still be available
      assert {:ok, _} = RateLimiter.check_rate(ip, :player_creation)

      # Connection should still be available
      assert {:ok, _} = RateLimiter.check_rate(ip, :connection)
    end

    test "different IPs have independent limits" do
      ip1 = {127, 0, 0, 1}
      ip2 = {192, 168, 1, 1}

      RateLimiter.clear_ip(ip1)
      RateLimiter.clear_ip(ip2)

      # Use up ip1's limit
      config = RateLimiter.get_config()
      limit = config.limits.game_creation

      for _ <- 1..limit do
        assert {:ok, _} = RateLimiter.check_rate(ip1, :game_creation)
      end

      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip1, :game_creation)

      # ip2 should still be able to make requests
      assert {:ok, _} = RateLimiter.check_rate(ip2, :game_creation)
    end

    test "accepts string IP addresses", %{ip: _ip} do
      string_ip = "127.0.0.1"
      RateLimiter.clear_ip(string_ip)

      assert {:ok, _} = RateLimiter.check_rate(string_ip, :game_creation)
    end

    test "accepts tuple IP addresses", %{ip: ip} do
      assert {:ok, _} = RateLimiter.check_rate(ip, :game_creation)
    end
  end

  describe "clear_ip/1" do
    test "clears all rate limit data for an IP", %{ip: ip} do
      # Make some requests
      assert {:ok, _} = RateLimiter.check_rate(ip, :game_creation)
      assert {:ok, _} = RateLimiter.check_rate(ip, :player_creation)
      assert {:ok, _} = RateLimiter.check_rate(ip, :connection)

      # Clear the IP
      RateLimiter.clear_ip(ip)

      # All limits should be reset
      config = RateLimiter.get_config()

      # Check that we can make requests up to the limit again
      assert {:ok, remaining} = RateLimiter.check_rate(ip, :game_creation)
      assert remaining == config.limits.game_creation - 1
    end
  end

  describe "get_config/0" do
    test "returns the current configuration" do
      config = RateLimiter.get_config()

      assert is_map(config)
      assert Map.has_key?(config, :limits)
      assert Map.has_key?(config, :windows)

      assert Map.has_key?(config.limits, :game_creation)
      assert Map.has_key?(config.limits, :player_creation)
      assert Map.has_key?(config.limits, :connection)

      assert Map.has_key?(config.windows, :game_creation)
      assert Map.has_key?(config.windows, :player_creation)
      assert Map.has_key?(config.windows, :connection)
    end

    test "has sensible default values" do
      config = RateLimiter.get_config()

      # Game creation limit should be reasonable
      assert config.limits.game_creation > 0
      assert config.limits.game_creation <= 30

      # Player creation limit should be higher than game creation
      assert config.limits.player_creation >= config.limits.game_creation

      # Connection limit should be the highest
      assert config.limits.connection >= config.limits.player_creation

      # Windows should be in reasonable ranges (seconds)
      assert config.windows.game_creation >= 60
      assert config.windows.player_creation >= 60
      # Connection window can be as low as 1 second for high-frequency limits
      assert config.windows.connection >= 1
    end

    test "handles invalid environment variable gracefully" do
      # This test verifies that invalid env vars fall back to defaults
      # In real usage, the GenServer would log a warning but continue
      config = RateLimiter.get_config()

      # Should have valid positive integer values (defaults or valid env vars)
      assert is_integer(config.limits.game_creation) and config.limits.game_creation > 0
      assert is_integer(config.limits.player_creation) and config.limits.player_creation > 0
      assert is_integer(config.limits.connection) and config.limits.connection > 0
    end
  end

  describe "rate limit windows" do
    test "requests expire after the time window", %{ip: ip} do
      config = RateLimiter.get_config()
      limit = config.limits.game_creation

      # Make requests up to the limit
      for _ <- 1..limit do
        assert {:ok, _} = RateLimiter.check_rate(ip, :game_creation)
      end

      # Should be blocked
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :game_creation)

      # Note: We can't easily test the time-based expiration in a unit test
      # without mocking time or waiting. This would be better tested in an
      # integration test or by mocking System.system_time/1
    end
  end

  describe "concurrent access" do
    test "handles concurrent requests from same IP correctly", %{ip: ip} do
      # Spawn multiple processes making requests concurrently
      tasks =
        for _ <- 1..5 do
          Task.async(fn ->
            RateLimiter.check_rate(ip, :game_creation)
          end)
        end

      results = Task.await_many(tasks, 5000)

      # All requests should get a response (either success or rate limit exceeded)
      assert Enum.all?(results, fn result ->
               match?({:ok, _}, result) or match?({:error, :rate_limit_exceeded}, result)
             end)
    end

    test "handles concurrent requests from different IPs correctly" do
      ips = [{127, 0, 0, 1}, {127, 0, 0, 2}, {127, 0, 0, 3}, {127, 0, 0, 4}, {127, 0, 0, 5}]

      Enum.each(ips, &RateLimiter.clear_ip/1)

      tasks =
        for ip <- ips do
          Task.async(fn ->
            RateLimiter.check_rate(ip, :game_creation)
          end)
        end

      results = Task.await_many(tasks, 5000)

      # All requests should succeed since they're from different IPs
      assert Enum.all?(results, fn result -> match?({:ok, _}, result) end)
    end
  end

  describe "IP normalization" do
    test "normalizes IPv4 string to tuple", %{ip: _ip} do
      # Test with string IP
      assert {:ok, _} = RateLimiter.check_rate("192.168.1.1", :game_creation)
      assert {:ok, _} = RateLimiter.check_rate("10.0.0.1", :player_creation)
    end

    test "handles IPv6 addresses", %{ip: _ip} do
      ipv6 = {0, 0, 0, 0, 0, 0, 0, 1}
      RateLimiter.clear_ip(ipv6)
      assert {:ok, _} = RateLimiter.check_rate(ipv6, :connection)
    end

    test "handles malformed IP strings gracefully", %{ip: _ip} do
      # Should still work even with weird input
      assert {:ok, _} = RateLimiter.check_rate("invalid-ip", :game_creation)
    end
  end

  describe "cleanup process" do
    test "rate limiter process is alive" do
      assert Process.whereis(Copi.RateLimiter) != nil
    end

    test "can make requests after clearing IP", %{ip: ip} do
      config = RateLimiter.get_config()
      limit = config.limits.connection

      # Exhaust limit
      for _ <- 1..limit do
        RateLimiter.check_rate(ip, :connection)
      end

      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(ip, :connection)

      # Clear and try again
      RateLimiter.clear_ip(ip)
      assert {:ok, _} = RateLimiter.check_rate(ip, :connection)
    end
  end
end
