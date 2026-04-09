defmodule CopiWeb.SecurityHeadersTest do
  use CopiWeb.ConnCase

  alias CopiWeb.SecurityHeaders

  test "browser pipeline includes form-action 'self' in CSP header", %{conn: conn} do
    conn = get(conn, "/")
    csp = get_resp_header(conn, "content-security-policy") |> List.first()
    assert csp =~ "form-action 'self'"
  end

  test "browser headers come from SecurityHeaders.browser_headers/0", %{conn: _conn} do
    csp = SecurityHeaders.browser_headers()["content-security-policy"]
    assert csp =~ "form-action 'self'"
    assert csp =~ "img-src 'self' data:"
  end
end