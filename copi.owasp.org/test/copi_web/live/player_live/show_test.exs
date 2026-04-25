defmodule CopiWeb.PlayerLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.DealtCard

  @game_attrs %{name: "show test game"}

  defp create_player(_) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    {:ok, player} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
    %{player: player}
  end

  defp create_game_with_dealt_card(game_name, card_ext_id) do
    {:ok, game} = Cornucopia.create_game(%{name: game_name, edition: "webapp"})
    {:ok, player} = Cornucopia.create_player(%{name: "Player One", game_id: game.id})

    {:ok, card} = Cornucopia.create_card(%{
      category: "C", value: card_ext_id, description: "D", edition: "webapp",
      version: "2.2", external_id: card_ext_id, language: "en", misc: "m",
      owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
      capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
    })

    dealt = Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
      player_id: player.id, card_id: card.id
    })

    {:ok, game} = Game.find(game.id)
    {game, player, dealt}
  end

  describe "Show - additional coverage" do
    setup [:create_player]

    test "handle_params redirects to /error for nonexistent player_id", %{conn: conn, player: _player} do
      assert {:error, {:redirect, %{to: "/error"}}} =
               live(conn, "/games/00000000000000000000000001/players/00000000000000000000000002")
    end

    test "handle_info :proceed_to_next_round advances rounds_played", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      send(show_live.pid, :proceed_to_next_round)
      :timer.sleep(100)

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
    end

    test "handle_info :proceed_to_next_round sets finished_at on last round", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, card} =
        Cornucopia.create_card(%{
          category: "C", value: "V", description: "D", edition: "webapp",
          version: "2.2", external_id: "ST1", language: "en", misc: "misc",
          owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
          capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
        })

      Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
        player_id: player.id, card_id: card.id, played_in_round: 1
      })

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      send(show_live.pid, :proceed_to_next_round)
      :timer.sleep(100)

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.finished_at != nil
    end

    test "next_round is no-op when round is open and cannot continue", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      html = render_click(show_live, "next_round", %{})
      assert is_binary(html)

      {:ok, unchanged_game} = Cornucopia.Game.find(game_id)
      assert unchanged_game.rounds_played == 0
    end

    test "next_round proceeds when majority continue votes reached", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      Copi.Repo.insert!(%Copi.Cornucopia.ContinueVote{player_id: player.id, game_id: game_id})

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      render_click(show_live, "next_round", %{})

      :timer.sleep(300)

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
    end

    test "helper functions return expected values", %{conn: _conn, player: _player} do
      alias CopiWeb.PlayerLive.Show

      assert Show.ordered_cards([]) == []
      assert Show.unplayed_cards([]) == []
      assert Show.played_cards([], 1) == []
      assert Show.card_played_in_round([], 1) == nil
      assert Show.round_closed?(%{players: [], rounds_played: 0}) == true

      player_with_unplayed = %{dealt_cards: [%{played_in_round: nil}]}
      refute Show.last_round?(%{players: [player_with_unplayed], rounds_played: 0})

      player_all_played = %{dealt_cards: [%{played_in_round: 1}]}
      assert Show.last_round?(%{players: [player_all_played], rounds_played: 0})

      assert Show.display_game_session("webapp")    == "Cornucopia Web Session:"
      assert Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("masvs")     == "Cornucopia Mobile Session:"
      assert Show.display_game_session("cumulus")   == "OWASP Cumulus Session:"
      assert Show.display_game_session("mlsec")     == "Elevation of MLSec Session:"
      assert Show.display_game_session("eop")       == "EoP Session:"
    end

    test "player_first/2 places current player first in list", %{conn: _conn, player: player} do
      alias CopiWeb.PlayerLive.Show
      other = %{id: "other-id"}
      current = %{id: player.id}
      sorted = Show.player_first([other, current], player)
      assert List.first(sorted).id == player.id
    end

    test "get_vote/2 returns nil when no matching vote", %{conn: _conn, player: player} do
      alias CopiWeb.PlayerLive.Show
      dealt = %{votes: []}
      assert Show.get_vote(dealt, player) == nil
    end

    test "get_vote/2 returns the matching vote", %{conn: _conn, player: player} do
      alias CopiWeb.PlayerLive.Show
      vote = %{player_id: player.id}
      dealt = %{votes: [vote]}
      assert Show.get_vote(dealt, player) == vote
    end

    test "next_round when round is closed and not last round advances rounds_played",
         %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, card1} =
        Cornucopia.create_card(%{
          category: "C", value: "V3", description: "D", edition: "webapp",
          version: "2.2", external_id: "NR_CLOSED1", language: "en", misc: "m",
          owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
          capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
        })

      {:ok, card2} =
        Cornucopia.create_card(%{
          category: "C", value: "V4", description: "D", edition: "webapp",
          version: "2.2", external_id: "NR_CLOSED2", language: "en", misc: "m",
          owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
          capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
        })

      Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
        player_id: player.id, card_id: card1.id, played_in_round: 1
      })

      Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
        player_id: player.id, card_id: card2.id, played_in_round: nil
      })

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      render_click(show_live, "next_round", %{})
      :timer.sleep(100)

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
      assert updated_game.finished_at == nil
    end

    test "next_round when round is closed and IS last round sets finished_at",
         %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, card} =
        Cornucopia.create_card(%{
          category: "C", value: "V5", description: "D", edition: "webapp",
          version: "2.2", external_id: "NR_LAST1", language: "en", misc: "m",
          owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
          capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
        })
      Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
        player_id: player.id, card_id: card.id, played_in_round: 1
      })

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      render_click(show_live, "next_round", %{})
      :timer.sleep(100)

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
      assert updated_game.finished_at != nil
    end

    test "toggle_continue_vote adds then removes a continue vote", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      render_click(show_live, "toggle_continue_vote", %{})
      :timer.sleep(100)

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert length(updated_game.continue_votes) == 1

      render_click(show_live, "toggle_continue_vote", %{})
      :timer.sleep(100)

      {:ok, updated_game2} = Cornucopia.Game.find(game_id)
      assert length(updated_game2.continue_votes) == 0
    end

    test "toggle_vote adds then removes a vote for a dealt card", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, card} =
        Cornucopia.create_card(%{
          category: "C", value: "TV1", description: "D", edition: "webapp",
          version: "2.2", external_id: "TV_CARD1", language: "en", misc: "m",
          owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
          capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
        })

      dealt = Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
        player_id: player.id, card_id: card.id, played_in_round: 1
      })

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      render_click(show_live, "toggle_vote", %{"dealt_card_id" => to_string(dealt.id)})
      :timer.sleep(100)

      {:ok, updated_dealt} = Copi.Cornucopia.DealtCard.find(to_string(dealt.id))
      assert length(updated_dealt.votes) == 1

      render_click(show_live, "toggle_vote", %{"dealt_card_id" => to_string(dealt.id)})
      :timer.sleep(100)

      {:ok, updated_dealt2} = Copi.Cornucopia.DealtCard.find(to_string(dealt.id))
      assert length(updated_dealt2.votes) == 0
    end
  end

  describe "toggle_vote authorization" do
    test "rejects cross-game vote and shows error flash", %{conn: conn} do
      {game1, player1, _dc1} = create_game_with_dealt_card("Auth Game One", "AUTH_G1_C1")
      {_game2, _player2, dc2} = create_game_with_dealt_card("Auth Game Two", "AUTH_G2_C1")

      {:ok, view, _html} = live(conn, "/games/#{game1.id}/players/#{player1.id}")
      render_click(view, "toggle_vote", %{"dealt_card_id" => to_string(dc2.id)})

      assert render(view) =~ "Invalid card selection"

      {:ok, refreshed_card} = DealtCard.find(dc2.id)
      assert refreshed_card.votes == []
    end

    test "allows a player to vote on a card belonging to their own game", %{conn: conn} do
      {game1, player1, dc1} = create_game_with_dealt_card("Auth Game Three", "AUTH_G3_C1")

      {:ok, view, _html} = live(conn, "/games/#{game1.id}/players/#{player1.id}")
      render_click(view, "toggle_vote", %{"dealt_card_id" => to_string(dc1.id)})

      {:ok, refreshed_card} = DealtCard.find(dc1.id)
      assert Enum.any?(refreshed_card.votes, fn v -> v.player_id == player1.id end)
    end
  end
end