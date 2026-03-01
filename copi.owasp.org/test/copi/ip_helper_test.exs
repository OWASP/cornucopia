defmodule Copi.IPHelperTest do
  use ExUnit.Case, async: true
  alias Copi.IPHelper

  setup do
    conn = %Plug.Conn{}
    {:ok, conn: conn}
  end

  describe "get_ip_from_conn/1" do
    test "extracts IP from X-Forwarded-For header", %{conn: conn} do
      conn = Plug.Conn.put_req_header(conn, "x-forwarded-for", "192.168.1.100, 10.0.0.1")
      assert IPHelper.get_ip_from_conn(conn) == {192, 168, 1, 100}
    end

    test "handles malformed X-Forwarded-For header", %{conn: conn} do
      conn = Plug.Conn.put_req_header(conn, "x-forwarded-for", "invalid-ip")
      conn = %{conn | remote_ip: {10, 0, 0, 1}}
      assert IPHelper.get_ip_from_conn(conn) == {10, 0, 0, 1}
    end

    test "falls back to remote_ip if X-Forwarded-For is missing", %{conn: conn} do
      conn = %{conn | remote_ip: {10, 0, 0, 1}}
      assert IPHelper.get_ip_from_conn(conn) == {10, 0, 0, 1}
    end

    test "falls back to localhost if remote_ip is missing", %{conn: conn} do
      assert IPHelper.get_ip_from_conn(conn) == {127, 0, 0, 1}
    end

    test "handles string IP addresses", %{conn: conn} do
      conn = %{conn | remote_ip: "10.0.0.1"}
      assert IPHelper.get_ip_from_conn(conn) == "10.0.0.1"
      
      conn2 = Plug.Conn.put_req_header(%Plug.Conn{}, "x-forwarded-for", "10.0.0.1")
      assert IPHelper.get_ip_from_conn(conn2) == {10, 0, 0, 1}
    end
  end

  describe "get_ip_source/1" do
    test "identifies forwarded IP", %{conn: conn} do
      conn = Plug.Conn.put_req_header(conn, "x-forwarded-for", "192.168.1.100")
      assert IPHelper.get_ip_source(conn) == {:forwarded, {192, 168, 1, 100}}
    end

    test "identifies remote IP", %{conn: conn} do
      conn = %{conn | remote_ip: {10, 0, 0, 1}}
      assert IPHelper.get_ip_source(conn) == {:remote, {10, 0, 0, 1}}
    end

    test "identifies lack of IP", %{conn: conn} do
      assert IPHelper.get_ip_source(conn) == {:none, nil}
    end

    test "identifies remote IP if it's a string", %{conn: conn} do
      conn = %{conn | remote_ip: "10.0.0.1"}
      assert IPHelper.get_ip_source(conn) == {:remote, "10.0.0.1"}
    end
  end

  describe "ip_to_string/1" do
    test "converts IPv4 tuple to string" do
      assert IPHelper.ip_to_string({192, 168, 1, 1}) == "192.168.1.1"
      assert IPHelper.ip_to_string({127, 0, 0, 1}) == "127.0.0.1"
    end

    test "converts IPv6 tuple to string" do
      assert IPHelper.ip_to_string({0, 0, 0, 0, 0, 0, 0, 1}) == "::1"
    end

    test "returns string if already a string" do
      assert IPHelper.ip_to_string("192.168.1.1") == "192.168.1.1"
    end

    test "inspects other types" do
      assert IPHelper.ip_to_string(:invalid) == ":invalid"
      assert IPHelper.ip_to_string(nil) == "nil"
    end

    test "handles malformed tuples" do
      assert IPHelper.ip_to_string({999, 999, 999, 999}) == "{999, 999, 999, 999}"
    end
  end

  describe "get_ip_from_socket/1 (LiveView)" do
    test "extracts IP from connect_info (Plug.Conn) X-Forwarded-For" do
      conn = %Plug.Conn{} |> Plug.Conn.put_req_header("x-forwarded-for", "10.0.0.1")
      socket = %Phoenix.LiveView.Socket{private: %{connect_info: conn}}
      assert IPHelper.get_ip_from_socket(socket) == {10, 0, 0, 1}
    end

    test "extracts IP from connect_info (Plug.Conn) peer_data" do
      conn = %Plug.Conn{private: %{peer_data: %{address: {10, 0, 0, 2}}}}
      socket = %Phoenix.LiveView.Socket{private: %{connect_info: conn}}
      assert IPHelper.get_ip_from_socket(socket) == {10, 0, 0, 2}
    end

    test "extracts IP from connect_info map x_headers" do
      socket = %Phoenix.LiveView.Socket{
        private: %{
          connect_info: %{
            x_headers: [{"x-forwarded-for", "10.0.0.3"}]
          }
        }
      }
      assert IPHelper.get_ip_from_socket(socket) == {10, 0, 0, 3}
    end

    test "extracts IP from connect_info map peer_data" do
      socket = %Phoenix.LiveView.Socket{
        private: %{
          connect_info: %{
            peer_data: %{address: {10, 0, 0, 4}}
          }
        }
      }
      assert IPHelper.get_ip_from_socket(socket) == {10, 0, 0, 4}
    end

    test "falls back to localhost if no info available" do
      socket = %Phoenix.LiveView.Socket{private: %{connect_info: nil}}
      assert IPHelper.get_ip_from_socket(socket) == {127, 0, 0, 1}
    end
    
    test "extracts IP from Phoenix.Socket transport_ip" do
      # Note: This is harder to test directly without starting actual processes
      # but we can simulate the dictionary access pattern
      socket = %Phoenix.Socket{transport_pid: self()}
      Process.put(:peer, {{10, 0, 0, 5}, 12345})
      assert IPHelper.get_ip_from_socket(socket) == {10, 0, 0, 5}
      
      socket2 = %Phoenix.Socket{transport_pid: nil}
      assert IPHelper.get_ip_from_socket(socket2) == {127, 0, 0, 1}
    end
  end
  
  describe "get_ip_from_connect_info/1" do
    test "extracts from x_headers" do
      info = %{x_headers: [{"x-forwarded-for", "10.0.0.5"}]}
      assert IPHelper.get_ip_from_connect_info(info) == {10, 0, 0, 5}
    end
    
    test "extracts from req_headers mapped values" do
       info = %{req_headers: %{"x-forwarded-for" => "10.0.0.6"}}
       assert IPHelper.get_ip_from_connect_info(info) == {10, 0, 0, 6}
    end

    test "extracts from peer_data" do
      info = %{peer_data: %{address: {10, 0, 0, 7}}}
      assert IPHelper.get_ip_from_connect_info(info) == {10, 0, 0, 7}
    end

    test "extracts from string based headers or nested maps" do
      info = %{headers: [{"x-forwarded-for", "10.0.0.8"}]}
      assert IPHelper.get_ip_from_connect_info(info) == {10, 0, 0, 8}
      
      info2 = %{request_headers: [{"x-forwarded-for", "10.0.0.9"}]}
      assert IPHelper.get_ip_from_connect_info(info2) == {10, 0, 0, 9}
      
      info3 = %{headers_in: {"x-forwarded-for", "10.0.0.10"}}
      assert IPHelper.get_ip_from_connect_info(info3) == nil

      info4 = %{x_headers: %{:"x-forwarded-for" => "10.0.0.11"}}
      assert IPHelper.get_ip_from_connect_info(info4) == {10, 0, 0, 11}
      
      info5 = %{}
      assert IPHelper.get_ip_from_connect_info(info5) == nil
    end

    test "handles malformed extract_first_ip inputs" do
      info = %{x_headers: [{"x-forwarded-for", "invalid"}]}
      assert IPHelper.get_ip_from_connect_info(info) == nil
      
      info2 = %{x_headers: [{"other", "10.0.0.1"}]}
      assert IPHelper.get_ip_from_connect_info(info2) == nil
    end
  end
end
