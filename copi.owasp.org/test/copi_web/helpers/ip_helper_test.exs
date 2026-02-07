defmodule CopiWeb.Helpers.IPHelperTest do
  use CopiWeb.ConnCase
  import Phoenix.LiveViewTest

  setup do
    # Clear rate limiter for all test IPs to prevent rate limit errors
    Copi.RateLimiter.clear_ip("127.0.0.1")
    Copi.RateLimiter.clear_ip("192.168.1.100")
    Copi.RateLimiter.clear_ip("10.0.0.1")
    Copi.RateLimiter.clear_ip("172.16.254.1")
    Copi.RateLimiter.clear_ip("2001:DB8:0:0:0:0:0:1")
    :ok
  end

  describe "get_connect_ip/1 with LiveView" do
    @tag peer_ip: {192, 168, 1, 100}
    test "extracts IPv4 address from socket during mount", %{conn: conn} do
      {:ok, view, _html} = live(conn, "/games")
      
      # Verify the IP was correctly extracted and stored
      socket = :sys.get_state(view.pid).socket
      assert socket.assigns.ip_address == "192.168.1.100"
    end

    @tag peer_ip: {8193, 3512, 0, 0, 0, 0, 0, 1}
    test "extracts IPv6 address from socket during mount", %{conn: conn} do
      {:ok, view, _html} = live(conn, "/games")
      
      socket = :sys.get_state(view.pid).socket
      assert socket.assigns.ip_address == "2001:DB8:0:0:0:0:0:1"
    end

    @tag peer_ip: {127, 0, 0, 1}
    test "handles localhost IPv4 address", %{conn: conn} do
      {:ok, view, _html} = live(conn, "/games")
      
      socket = :sys.get_state(view.pid).socket
      assert socket.assigns.ip_address == "127.0.0.1"
    end

    test "handles different IPv4 addresses", %{conn: conn} do
      test_cases = [
        {{10, 0, 0, 1}, "10.0.0.1"},
        {{172, 16, 254, 1}, "172.16.254.1"}
      ]
      
      for {address, expected} <- test_cases do
        conn = Plug.Conn.put_private(conn, :plug_connect_info, %{peer_data: %{address: address, port: 12345, ssl_cert: nil}})
        {:ok, view, _html} = live(conn, "/games")
        socket = :sys.get_state(view.pid).socket
        assert socket.assigns.ip_address == expected
        
        # Clear for next iteration
        Copi.RateLimiter.clear_ip(expected)
      end
    end
  end
end
