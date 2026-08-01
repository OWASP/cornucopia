defmodule CopiWeb.Plugs.LiveReloadSecurityHeadersPlugTest do
  use ExUnit.Case, async: true

  import Plug.Conn
  import Plug.Test

  alias CopiWeb.Plugs.LiveReloadSecurityHeadersPlug
  alias CopiWeb.SecurityHeaders

  test "live reload request receives live reload CSP headers" do
    conn = conn(:get, "/phoenix/live_reload/frame")
    conn = LiveReloadSecurityHeadersPlug.call(conn, LiveReloadSecurityHeadersPlug.init([]))

    assert get_resp_header(conn, "content-security-policy") ==
             [SecurityHeaders.live_reload_headers()["content-security-policy"]]
  end

  test "live reload CSP allows unsafe-inline scripts" do
    conn = conn(:get, "/phoenix/live_reload/frame")
    conn = LiveReloadSecurityHeadersPlug.call(conn, LiveReloadSecurityHeadersPlug.init([]))

    csp = get_resp_header(conn, "content-security-policy") |> List.first()
    assert csp =~ "script-src 'self' 'unsafe-inline'"
  end

  test "non-live-reload request does not receive live reload CSP headers" do
    conn = conn(:get, "/")
    conn = LiveReloadSecurityHeadersPlug.call(conn, LiveReloadSecurityHeadersPlug.init([]))

    assert get_resp_header(conn, "content-security-policy") == []
  end

  test "init/1 returns options unchanged" do
    assert LiveReloadSecurityHeadersPlug.init([]) == []
    assert LiveReloadSecurityHeadersPlug.init(foo: :bar) == [foo: :bar]
  end

  test "non-live-reload path is not affected by plug" do
    conn = conn(:get, "/games/new")
    conn = LiveReloadSecurityHeadersPlug.call(conn, LiveReloadSecurityHeadersPlug.init([]))

    assert get_resp_header(conn, "content-security-policy") == []
  end
end