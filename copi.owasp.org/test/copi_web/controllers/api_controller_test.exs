defmodule CopiWeb.ApiControllerTest do
  use CopiWeb.ConnCase
  alias CopiWeb.ApiController
  alias Copi.Repo
  alias Copi.Cornucopia
  alias Copi.Cornucopia.DealtCard

  defmodule GameStub do
    def find(id) do
      case Application.get_env(:copi, :api_game_stub_mode, :real) do
        :real -> Copi.Cornucopia.Game.find(id)
        :initial_not_found -> {:error, :not_found}
        :initial_transient -> {:error, :temporary}
        :second_not_found ->
          step = Application.get_env(:copi, :api_game_stub_step, 0)
          Application.put_env(:copi, :api_game_stub_step, step + 1)
          if step == 0, do: Copi.Cornucopia.Game.find(id), else: {:error, :not_found}
        :second_transient ->
          step = Application.get_env(:copi, :api_game_stub_step, 0)
          Application.put_env(:copi, :api_game_stub_step, step + 1)
          if step == 0, do: Copi.Cornucopia.Game.find(id), else: {:error, :temporary}
      end
    end
  end

  defmodule RepoStub do
    def update(changeset) do
      case Application.get_env(:copi, :api_repo_stub_mode, :real) do
        :real -> Copi.Repo.update(changeset)
        :error -> {:error, Ecto.Changeset.add_error(changeset, :played_in_round, "invalid")}
      end
    end
  end

  setup %{conn: conn} do
    old_game_mod = Application.get_env(:copi, :api_game_module)
    old_repo_mod = Application.get_env(:copi, :api_repo_module)
    old_game_mode = Application.get_env(:copi, :api_game_stub_mode)
    old_repo_mode = Application.get_env(:copi, :api_repo_stub_mode)
    old_step = Application.get_env(:copi, :api_game_stub_step)

    {:ok, game} = Cornucopia.create_game(%{name: "Test Game"})
    {:ok, player} = Cornucopia.create_player(%{name: "Test Player", game_id: game.id})

    {:ok, card} = Cornucopia.create_card(%{
      category: "Cornucopia", value: "A", description: "desc", misc: "misc",
      edition: "webapp", external_id: "1", language: "en", version: "1",
      owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
      capec: [], safecode: [], owasp_mastg: [], owasp_masvs: [],
      biml: "biml", url: "http://example.com"
    })

    {:ok, dealt_card} = Repo.insert(%DealtCard{player_id: player.id, card_id: card.id})

    on_exit(fn ->
      Application.put_env(:copi, :api_game_module, old_game_mod)
      Application.put_env(:copi, :api_repo_module, old_repo_mod)
      Application.put_env(:copi, :api_game_stub_mode, old_game_mode)
      Application.put_env(:copi, :api_repo_stub_mode, old_repo_mode)
      Application.put_env(:copi, :api_game_stub_step, old_step)
    end)

    conn = init_test_session(conn, %{
      "resume_player_session" => %{"game_id" => game.id, "player_id" => player.id}
    })

    %{conn: conn, game: game, player: player, dealt_card: dealt_card}
  end

  test "play_card success", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 200)["id"] == dealt_card.id

    updated = Repo.get(DealtCard, dealt_card.id)
    assert updated.played_in_round == 1
  end

  test "play_card requires a player session", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    conn =
      conn
      |> clear_session()
      |> put("/api/games/#{game.id}/players/#{player.id}/card", %{
        "dealt_card_id" => to_string(dealt_card.id)
      })

    assert json_response(conn, 401)["error"] == "Valid player session required"
    assert Repo.get(DealtCard, dealt_card.id).played_in_round == nil
  end

  test "play_card rejects a different player than the signed-in player", %{conn: conn, game: game} do
    {:ok, other_player} = Cornucopia.create_player(%{name: "Other Player", game_id: game.id})

    conn = put(conn, "/api/games/#{game.id}/players/#{other_player.id}/card", %{
      "dealt_card_id" => "1"
    })

    assert json_response(conn, 401)["error"] == "Valid player session required"
  end

  test "play_card fails if card already played", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    {:ok, _} = Repo.update(Ecto.Changeset.change(dealt_card, played_in_round: 1))

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 406)["error"] == "Card already played"
  end

  test "play_card rejects a player from another game", %{conn: conn, game: game} do
    {:ok, other_game} = Cornucopia.create_game(%{name: "Other Game"})
    {:ok, other_player} = Cornucopia.create_player(%{name: "Other", game_id: other_game.id})
    {:ok, card2} = Cornucopia.create_card(%{
      category: "C", value: "Q", description: "d", misc: "m",
      edition: "webapp", external_id: "99", language: "en", version: "1",
      owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
      capec: [], safecode: [], owasp_mastg: [], owasp_masvs: [],
      biml: "biml", url: "http://example.com"
    })
    {:ok, other_dealt} = Repo.insert(%DealtCard{player_id: other_player.id, card_id: card2.id})

    conn = put(conn, "/api/games/#{game.id}/players/#{other_player.id}/card", %{
      "game_id" => game.id,
      "player_id" => to_string(other_player.id),
      "dealt_card_id" => to_string(other_dealt.id)
    })

    assert json_response(conn, 401)["error"] == "Valid player session required"
  end

  test "play_card fails if player already played in round", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    {:ok, card2} = Cornucopia.create_card(%{
      category: "Cornucopia", value: "K", description: "desc", misc: "misc",
      edition: "webapp", external_id: "2", language: "en", version: "1",
      owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
      capec: [], safecode: [], owasp_mastg: [], owasp_masvs: [],
      biml: "biml", url: "http://example.com"
    })
    Repo.insert!(%DealtCard{player_id: player.id, card_id: card2.id, played_in_round: 1})

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 403)["error"] == "Player already played a card in this round"
  end

  test "play_card rejects a player id that does not match the session", %{conn: conn, game: game} do
    conn = put(conn, "/api/games/#{game.id}/players/99999/card", %{
      "game_id" => game.id,
      "player_id" => "99999",
      "dealt_card_id" => "1"
    })

    assert json_response(conn, 401)["error"] == "Valid player session required"
  end

  test "play_card rejects a game id that does not match the session", %{conn: conn, player: player, dealt_card: dealt_card} do
    conn = put(conn, "/api/games/00000000000000000000000099/players/#{player.id}/card", %{
      "game_id" => "00000000000000000000000099",
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 401)["error"] == "Valid player session required"
  end

  test "play_card returns 404 when dealt card id is missing for valid player", %{conn: conn, game: game, player: player} do
    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => "999999"
    })

    assert json_response(conn, 404)["error"] == "Could not find player and dealt card"
  end

  test "play_card returns 400 when dealt_card_id parameter is missing", %{conn: conn, game: game, player: player} do
    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id
    })

    assert json_response(conn, 400)["error"] == "Missing required parameter: dealt_card_id"
  end

  test "play_card returns 400 when params are missing game_id and player_id", %{conn: conn} do
    conn = ApiController.play_card(conn, %{})

    assert json_response(conn, 400)["error"] == "Invalid request parameters"
  end

  test "play_card returns 503 when initial game lookup is transient", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    Application.put_env(:copi, :api_game_module, GameStub)
    Application.put_env(:copi, :api_game_stub_mode, :initial_transient)

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 503)["error"] == "Temporary service issue. Please retry."
  end

  test "play_card returns 404 when game disappears after update", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    Application.put_env(:copi, :api_game_module, GameStub)
    Application.put_env(:copi, :api_repo_module, RepoStub)
    Application.put_env(:copi, :api_game_stub_mode, :second_not_found)
    Application.put_env(:copi, :api_repo_stub_mode, :real)
    Application.put_env(:copi, :api_game_stub_step, 0)

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 404)["error"] == "Could not find game"
  end

  test "play_card returns 503 when game reload after update is transient", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    Application.put_env(:copi, :api_game_module, GameStub)
    Application.put_env(:copi, :api_repo_module, RepoStub)
    Application.put_env(:copi, :api_game_stub_mode, :second_transient)
    Application.put_env(:copi, :api_repo_stub_mode, :real)
    Application.put_env(:copi, :api_game_stub_step, 0)

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 503)["error"] == "Temporary service issue. Please retry."
  end

  test "play_card returns 422 when dealt card update fails", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    Application.put_env(:copi, :api_game_module, GameStub)
    Application.put_env(:copi, :api_repo_module, RepoStub)
    Application.put_env(:copi, :api_game_stub_mode, :real)
    Application.put_env(:copi, :api_repo_stub_mode, :error)

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 422)["error"] == "Could not play card"
  end

  test "exchange stores an encrypted player capability in the session", %{conn: conn, game: game, player: player} do
    capability = CopiWeb.PlayerCapability.sign(game.id, player.id)

    conn =
      conn
      |> init_test_session(%{})
      |> post("/api/player-capabilities/exchange", %{"capability" => capability})

    assert json_response(conn, 200)["redirect_to"] == "/games/#{game.id}/players/#{player.id}"
    assert get_session(conn, "resume_player_session") == [
             %{"game_id" => game.id, "player_id" => player.id}
           ]
    assert get_resp_header(conn, "cache-control") == ["no-store"]
  end

  test "exchange adds a capability and returns a clean player URL", %{
    conn: conn,
    game: game,
    player: player
  } do
    {:ok, second_player} = Cornucopia.create_player(%{name: "Second Player", game_id: game.id})
    {:ok, other_game} = Cornucopia.create_game(%{name: "Other Game"})
    {:ok, other_player} = Cornucopia.create_player(%{name: "Other Player", game_id: other_game.id})

    existing_sessions = [
      %{"game_id" => game.id, "player_id" => player.id},
      %{"game_id" => other_game.id, "player_id" => other_player.id}
    ]

    capability = CopiWeb.PlayerCapability.sign(game.id, second_player.id)

    conn =
      conn
      |> init_test_session(%{"resume_player_session" => existing_sessions})
      |> post("/api/player-capabilities/exchange", %{"capability" => capability})

    clean_path = "/games/#{game.id}/players/#{second_player.id}"
    assert json_response(conn, 200)["redirect_to"] == clean_path
    refute response(conn, 200) =~ capability
    assert get_resp_header(conn, "cache-control") == ["no-store"]

    assert get_session(conn, "resume_player_session") == [
             %{"game_id" => game.id, "player_id" => second_player.id},
             %{"game_id" => game.id, "player_id" => player.id},
             %{"game_id" => other_game.id, "player_id" => other_player.id}
           ]

    assert Enum.any?(get_resp_header(conn, "set-cookie"), &String.contains?(&1, "max-age=604800"))
  end

  test "exchange rejects an invalid capability without changing existing sessions", %{
    conn: conn,
    game: game,
    player: player
  } do
    conn = post(conn, "/api/player-capabilities/exchange", %{"capability" => "invalid"})

    assert json_response(conn, 401)["error"] == "Invalid or expired player capability"
    assert get_session(conn, "resume_player_session") == %{
             "game_id" => game.id,
             "player_id" => player.id
           }
  end

  test "exchange rejects a capability older than five minutes", %{
    conn: conn,
    game: game,
    player: player
  } do
    expired_capability =
      Phoenix.Token.sign(
        CopiWeb.Endpoint,
        "player-capability",
        %{"purpose" => "player", "game_id" => game.id, "player_id" => player.id},
        signed_at: System.system_time(:second) - 301
      )

    conn =
      post(conn, "/api/player-capabilities/exchange", %{
        "capability" => expired_capability
      })

    assert json_response(conn, 401)["error"] == "Invalid or expired player capability"
  end

  test "exchange adds capabilities for the same game and other games", %{
    conn: conn,
    game: game,
    player: player
  } do
    {:ok, second_player} = Cornucopia.create_player(%{name: "Second Player", game_id: game.id})
    {:ok, other_game} = Cornucopia.create_game(%{name: "Other Game"})
    {:ok, other_player} = Cornucopia.create_player(%{name: "Other Game Player", game_id: other_game.id})

    second_capability = CopiWeb.PlayerCapability.sign(game.id, second_player.id)

    second_conn =
      conn
      |> post("/api/player-capabilities/exchange", %{"capability" => second_capability})

    assert json_response(second_conn, 200)["redirect_to"] == "/games/#{game.id}/players/#{second_player.id}"

    sessions_after_second = get_session(second_conn, "resume_player_session")

    assert sessions_after_second == [
             %{"game_id" => game.id, "player_id" => second_player.id},
             %{"game_id" => game.id, "player_id" => player.id}
           ]

    other_capability = CopiWeb.PlayerCapability.sign(other_game.id, other_player.id)

    other_conn =
      build_conn()
      |> init_test_session(%{"resume_player_session" => sessions_after_second})
      |> post("/api/player-capabilities/exchange", %{"capability" => other_capability})

    assert json_response(other_conn, 200)["redirect_to"] == "/games/#{other_game.id}/players/#{other_player.id}"

    assert get_session(other_conn, "resume_player_session") == [
             %{"game_id" => other_game.id, "player_id" => other_player.id},
             %{"game_id" => game.id, "player_id" => second_player.id},
             %{"game_id" => game.id, "player_id" => player.id}
           ]
  end

  test "session supports multiple players in one game and players in multiple games", %{
    conn: conn,
    game: game,
    player: player,
    dealt_card: dealt_card
  } do
    {:ok, second_player} = Cornucopia.create_player(%{name: "Second Player", game_id: game.id})
    second_dealt_card = Repo.insert!(%DealtCard{player_id: second_player.id, card_id: dealt_card.card_id})

    {:ok, other_game} = Cornucopia.create_game(%{name: "Other Game"})
    {:ok, other_player} = Cornucopia.create_player(%{name: "Other Game Player", game_id: other_game.id})
    other_dealt_card = Repo.insert!(%DealtCard{player_id: other_player.id, card_id: dealt_card.card_id})

    sessions = [
      %{"game_id" => game.id, "player_id" => player.id},
      %{"game_id" => game.id, "player_id" => second_player.id},
      %{"game_id" => other_game.id, "player_id" => other_player.id}
    ]

    second_player_conn =
      conn
      |> init_test_session(%{"resume_player_session" => sessions})
      |> put("/api/games/#{game.id}/players/#{second_player.id}/card", %{
        "dealt_card_id" => to_string(second_dealt_card.id)
      })

    assert json_response(second_player_conn, 200)["id"] == second_dealt_card.id

    other_game_conn =
      build_conn()
      |> init_test_session(%{"resume_player_session" => sessions})
      |> put("/api/games/#{other_game.id}/players/#{other_player.id}/card", %{
        "dealt_card_id" => to_string(other_dealt_card.id)
      })

    assert json_response(other_game_conn, 200)["id"] == other_dealt_card.id

    mismatched_pair_conn =
      build_conn()
      |> init_test_session(%{"resume_player_session" => sessions})
      |> put("/api/games/#{game.id}/players/#{other_player.id}/card", %{
        "dealt_card_id" => to_string(other_dealt_card.id)
      })

    assert json_response(mismatched_pair_conn, 401)["error"] == "Valid player session required"
  end

  test "exchange rejects requests without a capability", %{conn: conn, game: game, player: player} do
    conn = post(conn, "/api/player-capabilities/exchange", %{})

    assert json_response(conn, 400)["error"] == "Invalid player capability request"
    assert get_session(conn, "resume_player_session") == %{"game_id" => game.id, "player_id" => player.id}
  end

  test "exchange rejects a replay without changing the second session", %{conn: conn, game: game, player: player} do
    capability = CopiWeb.PlayerCapability.sign(game.id, player.id)

    first_conn =
      conn
      |> init_test_session(%{})
      |> post("/api/player-capabilities/exchange", %{"capability" => capability})

    assert json_response(first_conn, 200)["redirect_to"] == "/games/#{game.id}/players/#{player.id}"

    replay_conn =
      build_conn()
      |> init_test_session(%{})
      |> post("/api/player-capabilities/exchange", %{"capability" => capability})

    assert json_response(replay_conn, 401)["error"] == "Invalid or expired player capability"
    assert get_session(replay_conn, "resume_player_session") == nil
  end

  test "clear_player_session removes only the matching game and player pair", %{conn: conn, game: game, player: player} do
    {:ok, other_player} = Cornucopia.create_player(%{name: "Other Player", game_id: game.id})

    conn =
      conn
      |> init_test_session(%{
        "resume_player_session" => [
          %{"game_id" => game.id, "player_id" => player.id},
          %{"game_id" => game.id, "player_id" => other_player.id}
        ]
      })
      |> delete("/api/games/#{game.id}/players/#{player.id}/session")

    assert json_response(conn, 200)["ok"] == true
    assert get_session(conn, "resume_player_session") == [
             %{"game_id" => game.id, "player_id" => other_player.id}
           ]
    assert get_resp_header(conn, "cache-control") == ["no-store"]
  end

  test "clear_player_session deletes the session key when the last player session is removed", %{
    conn: conn,
    game: game,
    player: player
  } do
    conn =
      conn
      |> init_test_session(%{
        "resume_player_session" => [%{"game_id" => game.id, "player_id" => player.id}]
      })
      |> delete("/api/games/#{game.id}/players/#{player.id}/session")

    assert json_response(conn, 200)["ok"] == true
    assert get_session(conn, "resume_player_session") == nil
    assert get_resp_header(conn, "cache-control") == ["no-store"]
  end

  test "clear_player_session returns 400 for an invalid game id format", %{conn: conn} do
    conn =
      delete(
        conn,
        "/api/games/not-a-valid-ulid/players/00000000000000000000000001/session"
      )

    assert json_response(conn, 400)["error"] == "Invalid player session parameters"
    assert get_resp_header(conn, "cache-control") == ["no-store"]
  end

  test "clear_player_session returns 400 for an invalid player id format", %{conn: conn} do
    conn =
      delete(
        conn,
        "/api/games/00000000000000000000000001/players/not-a-valid-ulid/session"
      )

    assert json_response(conn, 400)["error"] == "Invalid player session parameters"
    assert get_resp_header(conn, "cache-control") == ["no-store"]
  end
end