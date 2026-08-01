defmodule CopiWeb.EndpointTest do
  use ExUnit.Case, async: true

  import Plug.Conn
  import Plug.Test

  alias CopiWeb.Plugs.LiveReloadSecurityHeadersPlug
  alias CopiWeb.SecurityHeaders

  test "endpoint configuration includes connect_info for LiveView socket" do
    config = CopiWeb.Endpoint.__sockets__()

    live_socket = Enum.find(config, fn
      {path, _, _} -> path == "/live"
      _ -> false
    end)

    assert live_socket != nil, "LiveView socket should be configured"

    {_path, _module, opts} = live_socket

    websocket_config = Keyword.get(opts, :websocket, [])
    connect_info = Keyword.get(websocket_config, :connect_info, [])

    assert is_list(connect_info), "WebSocket should have connect_info configured"
    assert length(connect_info) > 0, "WebSocket connect_info should not be empty"
  end

  test "endpoint is started and running" do
    assert Process.whereis(CopiWeb.Endpoint) != nil
  end

  test "live reload requests receive the shared CSP headers" do
    conn = conn(:get, "/phoenix/live_reload/frame")

    conn = LiveReloadSecurityHeadersPlug.call(conn, LiveReloadSecurityHeadersPlug.init([]))

    assert get_resp_header(conn, "content-security-policy") == [SecurityHeaders.live_reload_headers()["content-security-policy"]]
    assert SecurityHeaders.live_reload_headers()["content-security-policy"] =~ "script-src 'self' 'unsafe-inline'"
  end
end