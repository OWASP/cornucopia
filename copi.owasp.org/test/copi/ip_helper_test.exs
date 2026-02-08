defmodule Copi.IPHelperTest do
  use ExUnit.Case, async: true
  alias Copi.IPHelper

  describe "get_ip_from_socket/1 with LiveView socket" do
    test "extracts IP from LiveView socket with peer_data" do
      socket = %Phoenix.LiveView.Socket{
        private: %{
          connect_info: %{
            peer_data: %{address: {127, 0, 0, 1}, port: 12345}
          }
        }
      }

      assert IPHelper.get_ip_from_socket(socket) == {127, 0, 0, 1}
    end

    test "extracts IPv6 address from LiveView socket" do
      socket = %Phoenix.LiveView.Socket{
        private: %{
          connect_info: %{
            peer_data: %{address: {0, 0, 0, 0, 0, 0, 0, 1}, port: 12345}
          }
        }
      }

      assert IPHelper.get_ip_from_socket(socket) == {0, 0, 0, 0, 0, 0, 0, 1}
    end

    test "returns fallback IP when not available in LiveView socket" do
      socket = %Phoenix.LiveView.Socket{
        private: %{}
      }

      # Should return localhost fallback instead of raising
      assert IPHelper.get_ip_from_socket(socket) == {127, 0, 0, 1}
    end
  end

  describe "get_ip_from_conn/1" do
    test "extracts IP from Plug.Conn" do
      conn = %Plug.Conn{
        remote_ip: {192, 168, 1, 1}
      }

      assert IPHelper.get_ip_from_conn(conn) == {192, 168, 1, 1}
    end

    test "extracts IPv6 address from Plug.Conn" do
      conn = %Plug.Conn{
        remote_ip: {0, 0, 0, 0, 0, 0, 0, 1}
      }

      assert IPHelper.get_ip_from_conn(conn) == {0, 0, 0, 0, 0, 0, 0, 1}
    end

    test "extracts IP from X-Forwarded-For header when behind proxy" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "203.0.113.5, 198.51.100.17"}]
      }

      # Should use the leftmost (original client) IP
      assert IPHelper.get_ip_from_conn(conn) == {203, 0, 113, 5}
    end

    test "handles single IP in X-Forwarded-For header" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "203.0.113.5"}]
      }

      assert IPHelper.get_ip_from_conn(conn) == {203, 0, 113, 5}
    end

    test "falls back to remote_ip when X-Forwarded-For is invalid" do
      conn = %Plug.Conn{
        remote_ip: {192, 168, 1, 1},
        req_headers: [{"x-forwarded-for", "invalid-ip"}]
      }

      assert IPHelper.get_ip_from_conn(conn) == {192, 168, 1, 1}
    end

    test "falls back to remote_ip when no X-Forwarded-For header" do
      conn = %Plug.Conn{
        remote_ip: {192, 168, 1, 1},
        req_headers: []
      }

      assert IPHelper.get_ip_from_conn(conn) == {192, 168, 1, 1}
    end

    test "returns fallback IP when remote_ip is nil and no X-Forwarded-For" do
      conn = %Plug.Conn{
        remote_ip: nil,
        req_headers: []
      }

      # Should return localhost fallback instead of raising
      assert IPHelper.get_ip_from_conn(conn) == {127, 0, 0, 1}
    end
  end

  describe "ip_to_string/1" do
    test "converts IPv4 tuple to string" do
      assert IPHelper.ip_to_string({127, 0, 0, 1}) == "127.0.0.1"
    end

    test "converts IPv6 tuple to string" do
      ip_string = IPHelper.ip_to_string({0, 0, 0, 0, 0, 0, 0, 1})
      # IPv6 localhost can be represented as "::1" or "0:0:0:0:0:0:0:1"
      assert ip_string in ["::1", "0:0:0:0:0:0:0:1"]
    end

    test "converts another IPv4 address" do
      assert IPHelper.ip_to_string({192, 168, 1, 1}) == "192.168.1.1"
    end

    test "returns string as-is when given a string" do
      assert IPHelper.ip_to_string("127.0.0.1") == "127.0.0.1"
    end

    test "handles invalid IP gracefully" do
      result = IPHelper.ip_to_string(:invalid)
      assert is_binary(result)
    end

    test "converts various IPv4 addresses" do
      assert IPHelper.ip_to_string({10, 0, 0, 1}) == "10.0.0.1"
      assert IPHelper.ip_to_string({172, 16, 0, 1}) == "172.16.0.1"
      assert IPHelper.ip_to_string({203, 0, 113, 5}) == "203.0.113.5"
    end
  end

  describe "X-Forwarded-For header handling" do
    test "extracts IP from X-Forwarded-For with multiple proxies" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "203.0.113.5, 198.51.100.17, 192.0.2.1"}]
      }

      # Should use the leftmost (original client) IP
      assert IPHelper.get_ip_from_conn(conn) == {203, 0, 113, 5}
    end

    test "trims whitespace in X-Forwarded-For" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "  203.0.113.5  , 198.51.100.17"}]
      }

      assert IPHelper.get_ip_from_conn(conn) == {203, 0, 113, 5}
    end

    test "handles IPv6 in X-Forwarded-For" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "2001:db8::1"}]
      }

      result = IPHelper.get_ip_from_conn(conn)
      assert is_tuple(result)
      assert tuple_size(result) == 8
    end

    test "handles empty X-Forwarded-For header" do
      conn = %Plug.Conn{
        remote_ip: {192, 168, 1, 1},
        req_headers: [{"x-forwarded-for", ""}]
      }

      # Should fall back to remote_ip
      assert IPHelper.get_ip_from_conn(conn) == {192, 168, 1, 1}
    end
  end
end
