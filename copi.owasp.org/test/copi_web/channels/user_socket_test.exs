defmodule CopiWeb.UserSocketTest do
  use CopiWeb.ChannelCase, async: false
  alias Copi.RateLimiter

  setup do
    test_ip = {127, 0, 0, 1}
    RateLimiter.clear_ip(test_ip)
    {:ok, ip: test_ip}
  end

  describe "connect/3 with rate limiting" do
    test "allows connection under rate limit", %{ip: ip} do
      connect_info = %{peer_data: %{address: ip, port: 12345}}

      assert {:ok, _socket} = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info)
    end

    test "denies connection when rate limit exceeded", %{ip: ip} do
      config = RateLimiter.get_config()
      limit = config.limits.connection

      connect_info = %{peer_data: %{address: ip, port: 12345}}

      # Make connections up to the limit
      for _ <- 1..limit do
        assert {:ok, _} = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info)
      end

      # Next connection should be denied
      assert :error = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info)
    end

    test "handles missing peer_data gracefully" do
      connect_info = %{}

      # Should still work with fallback IP
      assert {:ok, _socket} = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info)
    end

    test "different IPs can connect independently" do
      ip1 = {127, 0, 0, 1}
      ip2 = {192, 168, 1, 1}

      RateLimiter.clear_ip(ip1)
      RateLimiter.clear_ip(ip2)

      connect_info1 = %{peer_data: %{address: ip1, port: 12345}}
      connect_info2 = %{peer_data: %{address: ip2, port: 12346}}

      # Both should be able to connect
      assert {:ok, _} = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info1)
      assert {:ok, _} = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info2)
    end

    test "rate limit only affects connections, not other actions", %{ip: ip} do
      config = RateLimiter.get_config()
      connection_limit = config.limits.connection

      connect_info = %{peer_data: %{address: ip, port: 12345}}

      # Exhaust connection limit
      for _ <- 1..connection_limit do
        assert {:ok, _} = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info)
      end

      assert :error = CopiWeb.UserSocket.connect(%{}, %Phoenix.Socket{}, connect_info)

      # But game creation should still work
      assert {:ok, _} = RateLimiter.check_rate(ip, :game_creation)

      # And player creation should still work
      assert {:ok, _} = RateLimiter.check_rate(ip, :player_creation)
    end
  end

  describe "id/1" do
    test "returns nil for anonymous sockets" do
      socket = %Phoenix.Socket{}
      assert CopiWeb.UserSocket.id(socket) == nil
    end
  end
end
