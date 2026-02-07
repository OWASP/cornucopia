defmodule CopiWeb.Helpers.IPHelperTest do
  use CopiWeb.ConnCase
  import Phoenix.LiveViewTest

  alias CopiWeb.Helpers.IPHelper

  describe "get_connect_ip/1" do
    test "extracts IPv4 address from socket", %{conn: conn} do
      # Simulate a connection from an IPv4 address
      conn = %{conn | remote_ip: {192, 168, 1, 100}}
      {:ok, view, _html} = live(conn, "/games")
      
      # Get the socket from the LiveView and extract IP
      socket = view.socket
      result = IPHelper.get_connect_ip(socket)
      
      assert result == "192.168.1.100"
    end

    test "extracts IPv6 address from socket", %{conn: conn} do
      # Simulate a connection from an IPv6 address
      conn = %{conn | remote_ip: {8193, 3512, 0, 0, 0, 0, 0, 1}}
      {:ok, view, _html} = live(conn, "/games")
      
      socket = view.socket
      result = IPHelper.get_connect_ip(socket)
      
      # IPv6 formatting should be hex with colons
      assert result == "2001:DB8:0:0:0:0:0:1"
    end

    test "handles localhost IPv4 address", %{conn: conn} do
      conn = %{conn | remote_ip: {127, 0, 0, 1}}
      {:ok, view, _html} = live(conn, "/games")
      
      result = IPHelper.get_connect_ip(view.socket)
      assert result == "127.0.0.1"
    end

    test "handles different IPv4 addresses", %{conn: conn} do
      test_cases = [
        {10, 0, 0, 1} => "10.0.0.1",
        {172, 16, 254, 1} => "172.16.254.1",
        {255, 255, 255, 255} => "255.255.255.255"
      ]
      
      for {address, expected} <- test_cases do
        conn = %{conn | remote_ip: address}
        {:ok, view, _html} = live(conn, "/games")
        result = IPHelper.get_connect_ip(view.socket)
        assert result == expected
      end
    end

    test "raises error when peer_data is nil" do
      # Create a socket without proper peer_data by using a custom mock
      socket = %Phoenix.LiveView.Socket{
        endpoint: CopiWeb.Endpoint,
        router: CopiWeb.Router,
        view: CopiWeb.GameLive.Index
      }
      
      assert_raise RuntimeError, ~r/Unable to determine IP address/, fn ->
        IPHelper.get_connect_ip(socket)
      end
    end
  end
end
