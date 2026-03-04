defmodule CopiWeb.PlayerLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia

  @game_attrs %{name: "show test game"}

  defp create_player(_) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    {:ok, player} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
    %{player: player}
  end

  describe "Show - additional coverage" do
    setup [:create_player]

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

      # A played card with no nil-round cards remaining → last_round? returns true
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

      # Start game but add no dealt cards and no continue votes → round_open? true, can_continue? false
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

      # 1 player + 1 continue vote → majority reached (1 > div(1,2) = 0), round_open? true
      Copi.Repo.insert!(%Copi.Cornucopia.ContinueVote{player_id: player.id, game_id: game_id})

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      render_click(show_live, "next_round", %{})

      # Wait for the async :proceed_to_next_round message (100ms delay + buffer)
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
      # With no players, no one is still to play → round_open? is false → round_closed? is true
      assert Show.round_closed?(%{players: [], rounds_played: 0}) == true

      assert Show.display_game_session("webapp")    == "Cornucopia Web Session:"
      assert Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("masvs")     == "Cornucopia Mobile Session:"
      assert Show.display_game_session("cumulus")   == "OWASP Cumulus Session:"
      assert Show.display_game_session("mlsec")     == "Elevation of MLSec Session:"
      assert Show.display_game_session("eop")       == "EoP Session:"
    end
  end
end
