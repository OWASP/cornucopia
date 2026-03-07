defmodule CopiWeb.PlayerLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest
  import ExUnit.CaptureLog

  alias Copi.Cornucopia

  @game_attrs %{name: "show test game"}

  defp create_player(_) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    {:ok, player} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
    %{player: player, game: game}
  end

  defp create_second_game(_) do
    {:ok, second_game} = Cornucopia.create_game(%{name: "Second Game"})
    %{second_game: second_game}
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

  describe "Security - IDOR Protection" do
    setup [:create_player, :create_second_game]

    test "allows access with correct game_id and player_id", %{conn: conn, player: player, game: game} do
      {:ok, _show_live, _html} = live(conn, "/games/#{game.id}/players/#{player.id}")
      # Should successfully mount without redirect
    end

    test "redirects when player accessed from wrong game context", %{conn: conn, player: player, second_game: second_game} do
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{second_game.id}/players/#{player.id}")
      end)
      
      assert log =~ "Security: Player #{player.id} access attempted from wrong game context"
      assert log =~ "URL game_id: #{second_game.id} vs actual game_id: #{player.game_id}"
    end

    test "redirects when player_id does not exist", %{conn: conn, game: game} do
      fake_player_id = "01KJQJAR0B57E96P7YJBDCEVYG"
      
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{game.id}/players/#{fake_player_id}")
      end)
      
      assert log =~ "Security: Player lookup failed for player_id: #{fake_player_id}"
    end

    test "redirects when game_id does not exist but player exists", %{conn: conn, player: player} do
      fake_game_id = "01KJQJAR0B57E96P7YJBDCEVYG"
      
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{fake_game_id}/players/#{player.id}")
      end)
      
      assert log =~ "Security: Player #{player.id} access attempted from wrong game context"
      assert log =~ "URL game_id: #{fake_game_id} vs actual game_id: #{player.game_id}"
    end

    test "redirects when both game_id and player_id do not exist", %{conn: conn} do
      fake_game_id = "01KJQJAR0B57E96P7YJBDCEVYG"
      fake_player_id = "01KJQJAR0B57E96P7YJBDCEVYF"
      
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{fake_game_id}/players/#{fake_player_id}")
      end)
      
      assert log =~ "Security: Player lookup failed for player_id: #{fake_player_id}"
    end

    test "handles malformed game_id parameter", %{conn: conn, player: player} do
      malformed_game_id = "invalid-game-id"
      
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{malformed_game_id}/players/#{player.id}")
      end)
      
      assert log =~ "Security: Player #{player.id} access attempted from wrong game context"
    end

    test "handles malformed player_id parameter", %{conn: conn, game: game} do
      malformed_player_id = "invalid-player-id"
      
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{game.id}/players/#{malformed_player_id}")
      end)
      
      assert log =~ "Security: Player lookup failed for player_id: #{malformed_player_id}"
    end

    test "security logging includes client IP address", %{conn: conn, player: player, second_game: second_game} do
      log = capture_log(fn ->
        assert {:error, {:redirect, %{to: "/error"}}} = 
          live(conn, "/games/#{second_game.id}/players/#{player.id}")
      end)
      
      assert log =~ "IP:"
    end
  end

  describe "Security - Regression Tests" do
    setup [:create_player]

    test "existing functionality still works after security fix", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, show_live, html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      
      # Verify the LiveView mounts successfully
      assert html =~ player.name
      assert render(show_live) =~ player.name
    end

    test "handle_info :proceed_to_next_round still works after security fix", %{conn: conn, player: player} do
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

    test "handle_event functionality still works after security fix", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      
      # Test that existing events still work
      html = render_click(show_live, "toggle_continue_vote", %{})
      assert is_binary(html)
    end
  end
end
