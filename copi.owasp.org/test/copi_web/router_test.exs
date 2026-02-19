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
      # Create actual game and player with valid ULIDs
      {:ok, game} = Copi.Cornucopia.create_game(%{name: "API Test", edition: "webapp"})
      {:ok, player} = Copi.Cornucopia.create_player(%{name: "API Player", game_id: game.id})
      
      conn = conn
        |> put_req_header("accept", "application/json")
        |> put("/api/games/#{game.id}/players/#{player.id}/card", %{"dealt_card_id" => "123"})

      # Invalid dealt_card_id should result in a client error, never a 500
      status = conn.status
      refute status == 500
      assert status in [404, 406]

      # V4.1.2, V16.5: Ensure a JSON error response is returned for invalid input
      response_body = json_response(conn, status)
      assert %{"error" => _} = response_body
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
