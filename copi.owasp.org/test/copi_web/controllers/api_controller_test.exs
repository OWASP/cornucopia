defmodule CopiWeb.ApiControllerTest do
  use CopiWeb.ConnCase
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

  setup do
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

    %{game: game, player: player, dealt_card: dealt_card}
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

  test "play_card fails if card already played", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    {:ok, _} = Repo.update(Ecto.Changeset.change(dealt_card, played_in_round: 1))

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 406)["error"] == "Card already played"
  end

  test "play_card returns 404 when dealt card not found for player", %{conn: conn, game: game} do
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

    assert json_response(conn, 404)["error"] == "Player not found in this game"
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

  test "play_card returns 404 when player_id doesn't belong to game", %{conn: conn, game: game} do
    conn = put(conn, "/api/games/#{game.id}/players/99999/card", %{
      "game_id" => game.id,
      "player_id" => "99999",
      "dealt_card_id" => "1"
    })

    assert json_response(conn, 404)["error"] == "Player not found in this game"
  end

  test "play_card returns 404 when game does not exist", %{conn: conn, player: player, dealt_card: dealt_card} do
    conn = put(conn, "/api/games/00000000000000000000000099/players/#{player.id}/card", %{
      "game_id" => "00000000000000000000000099",
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 404)["error"] == "Could not find game"
  end

  test "play_card returns 404 when dealt card id is missing for valid player", %{conn: conn, game: game, player: player} do
    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => "999999"
    })

    assert json_response(conn, 404)["error"] == "Could not find player and dealt card"
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
end