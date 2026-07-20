defmodule CopiWeb.PlayerHandoffControllerTest do
  use CopiWeb.ConnCase, async: false

  alias Copi.Cornucopia
  alias CopiWeb.PlayerHandoff
  alias CopiWeb.PlayerSessions

  setup do
    {:ok, game} = Cornucopia.create_game(%{name: "Handoff Game"})
    {:ok, player} = Cornucopia.create_player(%{name: "Handoff Player", game_id: game.id})

    %{game: game, player: player}
  end

  test "redeems a handoff into a renewed player session", %{
    conn: conn,
    game: game,
    player: player
  } do
    token = PlayerHandoff.sign(game.id, player.id)
    conn = get(conn, "/player-handoffs/#{token}")

    assert redirected_to(conn) == "/games/#{game.id}/players/#{player.id}"

    assert PlayerSessions.authorized?(
             get_session(conn, "resume_player_session"),
             game.id,
             player.id
           )

    assert get_resp_header(conn, "cache-control") == ["no-store"]
  end

  test "preserves other player sessions when redeeming", %{conn: conn, game: game, player: player} do
    {:ok, other_player} =
      Cornucopia.create_player(%{name: "Other Player", game_id: game.id})

    token = PlayerHandoff.sign(game.id, player.id)

    conn =
      conn
      |> init_test_session(%{
        "resume_player_session" => [
          %{"game_id" => game.id, "player_id" => other_player.id}
        ]
      })
      |> get("/player-handoffs/#{token}")

    sessions = get_session(conn, "resume_player_session")
    assert PlayerSessions.authorized?(sessions, game.id, player.id)
    assert PlayerSessions.authorized?(sessions, game.id, other_player.id)
  end

  test "rejects a replay without granting a session", %{conn: conn, game: game, player: player} do
    token = PlayerHandoff.sign(game.id, player.id)

    assert conn |> get("/player-handoffs/#{token}") |> redirected_to() ==
             "/games/#{game.id}/players/#{player.id}"

    replay_conn = build_conn() |> get("/player-handoffs/#{token}")

    assert redirected_to(replay_conn) == "/games"
    assert Phoenix.Flash.get(replay_conn.assigns.flash, :error) =~ "invalid, expired"
    assert get_session(replay_conn, "resume_player_session") == nil
    assert get_resp_header(replay_conn, "cache-control") == ["no-store"]
  end

  test "rejects a tampered token", %{conn: conn, game: game, player: player} do
    token = PlayerHandoff.sign(game.id, player.id) <> "tampered"
    conn = get(conn, "/player-handoffs/#{token}")

    assert redirected_to(conn) == "/games"
    assert get_session(conn, "resume_player_session") == nil
  end

  test "rejects a player capability from another purpose", %{
    conn: conn,
    game: game,
    player: player
  } do
    token = CopiWeb.PlayerCapability.sign(game.id, player.id)
    conn = get(conn, "/player-handoffs/#{token}")

    assert redirected_to(conn) == "/games"
    assert get_session(conn, "resume_player_session") == nil
  end

  test "rejects signed malformed identifiers", %{conn: conn} do
    token = PlayerHandoff.sign("invalid-game", "invalid-player")
    conn = get(conn, "/player-handoffs/#{token}")

    assert redirected_to(conn) == "/games"
    assert get_session(conn, "resume_player_session") == nil
  end

  test "rejects a signed player and game mismatch", %{conn: conn, player: player} do
    {:ok, other_game} = Cornucopia.create_game(%{name: "Other Game"})
    token = PlayerHandoff.sign(other_game.id, player.id)
    conn = get(conn, "/player-handoffs/#{token}")

    assert redirected_to(conn) == "/games"
    assert get_session(conn, "resume_player_session") == nil
  end
end
