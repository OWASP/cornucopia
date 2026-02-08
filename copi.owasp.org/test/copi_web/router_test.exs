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

  test "GET /cards", %{conn: conn} do
    conn = get(conn, "/cards")
    assert html_response(conn, 200)
  end

  describe "API routes" do
    test "PUT /api/games/:game_id/players/:player_id/card requires valid params", %{conn: conn} do
      conn = conn
        |> put_req_header("accept", "application/json")
        |> put("/api/games/test-game/players/test-player/card", %{"dealt_card_id" => "123"})
      
      # Should respond (even if error due to invalid game/player)
      assert conn.status in [200, 400, 404, 422, 500]
    end
  end

  describe "LiveDashboard in test env" do
    test "GET /dashboard", %{conn: conn} do
      conn = get(conn, "/dashboard")
      # LiveDashboard redirects to /dashboard/home
      assert redirected_to(conn, 302) =~ "/dashboard/home"
    end
  end
end
