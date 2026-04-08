defmodule CopiWeb.SecurityHeadersTest do
  use CopiWeb.ConnCase

  test "browser pipeline includes form-action 'self' in CSP header", %{conn: conn} do
    conn = get(conn, "/")
    csp = get_resp_header(conn, "content-security-policy") |> List.first()
    assert csp =~ "form-action 'self'"
  end
end