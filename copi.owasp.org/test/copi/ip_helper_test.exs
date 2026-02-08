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

    test "raises error when IP not available in LiveView socket" do
      socket = %Phoenix.LiveView.Socket{
        private: %{}
      }

      assert_raise RuntimeError, "Unable to determine IP address from socket", fn ->
        IPHelper.get_ip_from_socket(socket)
      end
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

    test "raises error when remote_ip is nil" do
      conn = %Plug.Conn{
        remote_ip: nil
      }

      assert_raise RuntimeError, "Unable to determine IP address from connection", fn ->
        IPHelper.get_ip_from_conn(conn)
      end
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
  end
end
