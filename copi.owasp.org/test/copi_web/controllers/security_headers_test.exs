defmodule CopiWeb.SecurityHeadersTest do
  use CopiWeb.ConnCase

  describe "Content-Security-Policy header" do
    test "home page includes form-action directive", %{conn: conn} do
      conn = get(conn, "/")
      csp = get_resp_header(conn, "content-security-policy") |> List.first()
      assert csp =~ "form-action 'self'"
    end

    test "home page restricts all sources to same origin", %{conn: conn} do
      conn = get(conn, "/")
      csp = get_resp_header(conn, "content-security-policy") |> List.first()
      assert csp =~ "default-src 'self'"
      assert csp =~ "script-src 'self'"
      assert csp =~ "frame-ancestors 'self'"
      assert csp =~ "base-uri 'self'"
      assert csp =~ "object-src 'self'"
    end

    test "cards page also sends the CSP header", %{conn: conn} do
      conn = get(conn, "/cards")
      csp = get_resp_header(conn, "content-security-policy") |> List.first()
      assert csp =~ "form-action 'self'"
    end

    test "csp header is consistent across routes", %{conn: conn} do
      csp_home  = conn |> get("/") |> get_resp_header("content-security-policy") |> List.first()
      csp_cards = conn |> get("/cards") |> get_resp_header("content-security-policy") |> List.first()
      assert csp_home == csp_cards
    end

    test "style-src allows unsafe-inline for rendering", %{conn: conn} do
      conn = get(conn, "/")
      csp = get_resp_header(conn, "content-security-policy") |> List.first()
      assert csp =~ "style-src 'self' 'unsafe-inline'"
    end
  end
end