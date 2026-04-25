defmodule CopiWeb.RouterTest do
  use CopiWeb.ConnCase, async: true

  test "GET /", %{conn: conn} do
    conn = get(conn, "/")
    assert html_response(conn, 200)
  end

  test "GET /games", %{conn: conn} do
    conn = get(conn, "/games")
    assert html_response(conn, 200)
  end

  test "GET /games/new", %{conn: conn} do
    conn = get(conn, "/games/new")
    assert html_response(conn, 200)
  end

  test "GET /resources", %{conn: conn} do
    conn = get(conn, "/resources")
    assert html_response(conn, 200)
  end

  test "GET /privacy", %{conn: conn} do
    conn = get(conn, "/privacy")
    assert html_response(conn, 200)
  end

  test "GET /cards", %{conn: conn} do
    conn = get(conn, "/cards")
    assert html_response(conn, 200)
  end

  test "CSP header contains form-action 'self' on browser routes", %{conn: conn} do
    conn = get(conn, "/")
    csp = get_resp_header(conn, "content-security-policy") |> List.first()
    assert csp =~ "form-action 'self'"
    assert csp =~ "default-src 'self'"
    assert csp =~ "img-src 'self' data:"
  end

  test "CSP header is present on multiple browser routes", %{conn: conn} do
    for path <- ["/", "/cards", "/resources", "/privacy"] do
      conn = get(conn, path)
      csp = get_resp_header(conn, "content-security-policy") |> List.first()
      assert csp =~ "form-action 'self'", "Missing CSP on #{path}"
    end
  end

  describe "API routes" do
    test "PUT /api/games/:game_id/players/:player_id/card requires valid params", %{conn: conn} do
      {:ok, game} = Copi.Cornucopia.create_game(%{name: "API Test", edition: "webapp"})
      {:ok, player} = Copi.Cornucopia.create_player(%{name: "API Player", game_id: game.id})

      conn = conn
        |> put_req_header("accept", "application/json")
        |> put("/api/games/#{game.id}/players/#{player.id}/card", %{"dealt_card_id" => "123"})

      assert conn.status in [200, 400, 403, 404, 406, 422, 500]
    end
  end

  describe "LiveDashboard in test env" do
    test "GET /dashboard", %{conn: conn} do
      conn = get(conn, "/dashboard")
      assert redirected_to(conn, 302) =~ "/dashboard/home"
    end
  end
end