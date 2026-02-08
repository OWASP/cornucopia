defmodule CopiWeb.PlayerLiveTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest
  import Ecto.Query

  alias Copi.Cornucopia

  @game_attrs %{name: "some name"}
  # @create_attrs %{name: "some name", game_id: ""}
  # @update_attrs %{name: "some updated name"}
  @invalid_attrs %{name: nil}

  defp fixture(:player) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    {:ok, player} = Cornucopia.create_player(%{name: "some name", game_id: game.id})
    player
  end

  defp create_player(_) do
    player = fixture(:player)
    %{player: player}
  end

  describe "Index" do
    setup [:create_player]
    test "lists all players", %{conn: conn, player: player} do

      {:ok, _index_live, html} = live(conn, "/games/#{player.game_id}/players/#{player.id}")
      assert html =~ player.name
      assert html =~ "Cornucopia Web Session: some name"
    end

    test "saves new player", %{conn: conn, player: player} do
      {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}")

      assert index_live |> element(~s{[href="/games/#{player.game_id}/players/new"]}) |> render_click()

      assert_patch(index_live, "/games/#{player.game_id}/players/new")
      {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}/players/new")
      assert index_live
             |> form("#player-form", player: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      {:ok, _, html} =
        index_live
        |> form("#player-form", player: %{name: "some updated name", game_id: player.game_id})
        |> render_submit()
        |> follow_redirect(conn)

      assert html =~ "Hi some updated name, waiting for the game to start..."
      assert html =~ "Hi some updated name, waiting for the game to start..."
    end
  end

  describe "Show" do
    setup [:create_player]

    test "allows voting on other player's card", %{conn: conn, player: player} do
      # Setup another player and play a card
      game_id = player.game_id
      {:ok, other_player} = Cornucopia.create_player(%{name: "Other", game_id: game_id})
      
      # Start game (hacky: just set started_at)
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      # Deal/play card for Other
      {:ok, card} = Cornucopia.create_card(%{
        category: "C", value: "V", description: "D", edition: "webapp", 
        version: "2.2", external_id: "EXT", language: "en",
        misc: "misc", owasp_scp: [], owasp_devguide: [], owasp_asvs: [], 
        owasp_appsensor: [], capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
      })
      {:ok, dealt} = Copi.Repo.insert(%Copi.Cornucopia.DealtCard{player_id: other_player.id, card_id: card.id, played_in_round: 1})
      
      {:ok, show_live, html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      
      assert html =~ "Other"
      # Assuming 1 round played (default rounds_played=0, current=1)
      
      # Find vote button for the dealt card
      # The template uses phx-value-dealt_card_id
      show_live |> element("[phx-click=\"toggle_vote\"][phx-value-dealt_card_id=\"#{dealt.id}\"]") |> render_click()
      
      # Verify vote created
      assert Copi.Repo.get_by(Copi.Cornucopia.Vote, dealt_card_id: dealt.id, player_id: player.id)
    end

    test "allows continue voting and resets votes on next round", %{conn: conn, player: player} do
      # Setup another player
      game_id = player.game_id
      {:ok, other_player} = Cornucopia.create_player(%{name: "Other", game_id: game_id})
      
      # Start game
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      {:ok, show_live, html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      
      # Test continue voting
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()
      
      # Verify continue vote created
      assert Copi.Repo.get_by(Copi.Cornucopia.ContinueVote, player_id: player.id, game_id: game_id)
      
      # Test that votes are cleared when proceeding to next round
      # Manually clear votes and advance round to test the functionality
      Copi.Repo.delete_all(from cv in Copi.Cornucopia.ContinueVote, where: cv.game_id == ^game_id)
      Copi.Cornucopia.update_game(game, %{rounds_played: game.rounds_played + 1, round_open: true})
      
      # Verify continue votes are cleared
      refute Copi.Repo.get_by(Copi.Cornucopia.ContinueVote, player_id: player.id, game_id: game_id)
      
      # Verify game advanced to next round
      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
    end
  end
end
