defmodule Copi.IPHelperTest do
  use ExUnit.Case, async: true
  alias Copi.IPHelper

describe "additional safe coverage" do
  test "get_ip_from_conn with multiple unrelated headers" do
    conn = %Plug.Conn{
      remote_ip: {10, 0, 0, 1},
      req_headers: [
        {"content-type", "application/json"},
        {"accept", "*/*"}
      ]
    }

    assert IPHelper.get_ip_from_conn(conn) == {10, 0, 0, 1}
  end

  test "get_ip_from_conn prefers x-forwarded-for over remote_ip" do
    conn = %Plug.Conn{
      remote_ip: {10, 0, 0, 1},
      req_headers: [{"x-forwarded-for", "8.8.8.8"}]
    }

    assert IPHelper.get_ip_from_conn(conn) == {8, 8, 8, 8}
  end
end

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

  describe "get_ip_source/1" do
    test "returns {:forwarded, ip} when X-Forwarded-For header is present" do
      conn = %Plug.Conn{
        remote_ip: {10, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "203.0.113.5"}]
      }
      assert IPHelper.get_ip_source(conn) == {:forwarded, {203, 0, 113, 5}}
    end

    test "returns {:remote, ip} when only remote_ip is available" do
      conn = %Plug.Conn{
        remote_ip: {10, 0, 0, 1},
        req_headers: []
      }
      assert IPHelper.get_ip_source(conn) == {:remote, {10, 0, 0, 1}}
    end

    test "returns {:remote, ip} for a tuple remote_ip" do
      conn = %Plug.Conn{
        remote_ip: {192, 168, 1, 100},
        req_headers: [{"accept", "application/json"}]
      }
      assert IPHelper.get_ip_source(conn) == {:remote, {192, 168, 1, 100}}
    end

    test "returns {:none, nil} when no IP information available" do
      conn = %Plug.Conn{
        remote_ip: nil,
        req_headers: []
      }
      assert IPHelper.get_ip_source(conn) == {:none, nil}
    end

    test "returns {:forwarded, ip} with multiple proxies" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "8.8.8.8, 10.0.0.1"}]
      }
      assert IPHelper.get_ip_source(conn) == {:forwarded, {8, 8, 8, 8}}
    end
  end

  describe "get_ip_from_connect_info/1" do
    test "extracts IP from peer_data in connect_info" do
      connect_info = %{peer_data: %{address: {127, 0, 0, 1}, port: 12345}}
      assert IPHelper.get_ip_from_connect_info(connect_info) == {127, 0, 0, 1}
    end

    test "extracts IP from x_headers map in connect_info" do
      connect_info = %{
        x_headers: %{"x-forwarded-for" => "203.0.113.5"}
      }
      assert IPHelper.get_ip_from_connect_info(connect_info) == {203, 0, 113, 5}
    end

    test "extracts IP from x_headers list in connect_info" do
      connect_info = %{
        x_headers: [{"x-forwarded-for", "203.0.113.10"}]
      }
      assert IPHelper.get_ip_from_connect_info(connect_info) == {203, 0, 113, 10}
    end

    test "extracts IP from req_headers list in connect_info" do
      connect_info = %{
        req_headers: [{"x-forwarded-for", "198.51.100.1"}]
      }
      assert IPHelper.get_ip_from_connect_info(connect_info) == {198, 51, 100, 1}
    end

    test "returns nil when no IP info available" do
      connect_info = %{}
      assert IPHelper.get_ip_from_connect_info(connect_info) == nil
    end

    test "returns nil when peer_data has no address" do
      connect_info = %{peer_data: %{}}
      assert IPHelper.get_ip_from_connect_info(connect_info) == nil
    end

    test "returns nil when x_headers is nil" do
      connect_info = %{x_headers: nil}
      assert IPHelper.get_ip_from_connect_info(connect_info) == nil
    end

    test "handles atom key in x_headers list" do
      connect_info = %{
        x_headers: [{:"x-forwarded-for", "10.1.2.3"}]
      }
      assert IPHelper.get_ip_from_connect_info(connect_info) == {10, 1, 2, 3}
    end

    test "handles x_headers as a plain binary string" do
      connect_info = %{x_headers: "10.5.6.7"}
      assert IPHelper.get_ip_from_connect_info(connect_info) == {10, 5, 6, 7}
    end

    test "handles x_headers map with atom key" do
      connect_info = %{
        x_headers: %{"x-forwarded-for" => "172.16.0.1"}
      }
      assert IPHelper.get_ip_from_connect_info(connect_info) == {172, 16, 0, 1}
    end
  end

  describe "get_ip_from_socket/1 with LiveView connect_info as Plug.Conn" do
    test "extracts IP from LiveView socket when connect_info is a Plug.Conn" do
      conn = %Plug.Conn{
        remote_ip: {10, 20, 30, 40},
        req_headers: []
      }

      socket = %Phoenix.LiveView.Socket{
        private: %{connect_info: conn}
      }

      assert IPHelper.get_ip_from_socket(socket) == {10, 20, 30, 40}
    end

    test "extracts forwarded IP when connect_info is a Plug.Conn with X-Forwarded-For" do
      conn = %Plug.Conn{
        remote_ip: {127, 0, 0, 1},
        req_headers: [{"x-forwarded-for", "5.6.7.8"}]
      }

      socket = %Phoenix.LiveView.Socket{
        private: %{connect_info: conn}
      }

      assert IPHelper.get_ip_from_socket(socket) == {5, 6, 7, 8}
    end

    test "extracts IP from connect_info with x_headers" do
      socket = %Phoenix.LiveView.Socket{
        private: %{
          connect_info: %{
            x_headers: [{"x-forwarded-for", "9.8.7.6"}]
          }
        }
      }

      assert IPHelper.get_ip_from_socket(socket) == {9, 8, 7, 6}
    end

    test "extracts IP from connect_info with req_headers" do
      socket = %Phoenix.LiveView.Socket{
        private: %{
          connect_info: %{
            req_headers: [{"x-forwarded-for", "11.22.33.44"}]
          }
        }
      }

      assert IPHelper.get_ip_from_socket(socket) == {11, 22, 33, 44}
    end
  end
end
