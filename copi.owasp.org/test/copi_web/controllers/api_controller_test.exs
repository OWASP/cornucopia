defmodule CopiWeb.ApiControllerTest do
  use CopiWeb.ConnCase
  alias Copi.Repo
  alias Copi.Cornucopia
  alias Copi.Cornucopia.DealtCard

  setup do
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

    # We need to reload game to ensure preloads work if Game.find relies on them being associated
    # But usually tests run in transaction. Game.find likely does a fresh query.

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
    # Play it first
    {:ok, _} = Repo.update(Ecto.Changeset.change(dealt_card, played_in_round: 1))

    conn = put(conn, "/api/games/#{game.id}/players/#{player.id}/card", %{
      "game_id" => game.id,
      "player_id" => player.id,
      "dealt_card_id" => to_string(dealt_card.id)
    })

    assert json_response(conn, 406)["error"] == "Card already played"
  end

  test "play_card fails if player already played in round", %{conn: conn, game: game, player: player, dealt_card: dealt_card} do
    # Create another card and mark it as played in this round (0 + 1 => 1)
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
end
