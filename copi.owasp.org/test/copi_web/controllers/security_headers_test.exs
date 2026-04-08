defmodule CopiWeb.SecurityHeadersTest do
  use CopiWeb.ConnCase

  test "includes content security policy header with form-action directive", %{conn: conn} do
    conn = get(conn, "/")
    csp = get_resp_header(conn, "content-security-policy") |> List.first()
    assert csp =~ "form-action 'self'"
  end

  test "csp header restricts all sources to same origin", %{conn: conn} do
    conn = get(conn, "/")
    csp = get_resp_header(conn, "content-security-policy") |> List.first()
    assert csp =~ "default-src 'self'"
    assert csp =~ "script-src 'self'"
    assert csp =~ "frame-ancestors 'self'"
  end
end