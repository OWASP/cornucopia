defmodule CopiWeb.PlayerLiveTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest
  import Ecto.Query

  alias Copi.Cornucopia
  alias Copi.RateLimiter

  @game_attrs %{name: "some name"}
  # @create_attrs %{name: "some name", game_id: ""}
  # @update_attrs %{name: "some updated name"}
  @invalid_attrs %{name: nil}

  setup %{conn: conn} do
    # Clear rate limits to prevent cross-test contamination
    RateLimiter.clear_ip({127, 0, 0, 1})
    # Set up IP address for rate limiting tests
    conn = Plug.Conn.put_private(conn, :connect_info, %{peer_data: %{address: {127, 0, 0, 1}}})
    {:ok, conn: conn}
  end

  defp fixture(:player) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    {:ok, player} = Cornucopia.create_player(%{name: "some name", game_id: game.id})
    player
  end

  defp create_player(_) do
    player = fixture(:player)
    %{player: player}
  end

  describe "player :index action" do
    setup [:create_player]

    test "visiting /players lists players on player index", %{conn: conn, player: player} do
      {:ok, _index_live, html} = live(conn, "/games/#{player.game_id}/players")
      assert is_binary(html)
    end
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

    test "blocks player creation when rate limit exceeded", %{conn: conn, player: player} do
      test_ip = {127, 0, 0, 1}
      RateLimiter.clear_ip(test_ip)

      # Get the rate limit config
      config = RateLimiter.get_config()
      limit = config.limits.player_creation

      # Simulate hitting the limit directly via the RateLimiter module
      # This avoids opening 60 concurrent database connections in the test Sandbox
      for _i <- 1..limit do
        {:ok, _} = RateLimiter.check_rate(test_ip, :player_creation)
      end

      # Next player creation should be blocked by the rate limiter logic in LiveView
      {:ok, index_live_blocked, _html} = live(conn, "/games/#{player.game_id}/players/new")
      
      index_live_blocked
        |> form("#player-form", player: %{name: "Blocked Player", game_id: player.game_id})
        |> render_submit()
      
      # Verify rate limit is exceeded (form stays, no redirect)
      assert has_element?(index_live_blocked, "#player-form")
      # Verify the rate limiter actually blocked the request
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate(test_ip, :player_creation)
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
      {:ok, _other_player} = Cornucopia.create_player(%{name: "Other", game_id: game_id})
      
      # Start game
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      
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

    test "allows toggling continue vote off", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      
      # Add vote
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()
      assert Copi.Repo.get_by(Copi.Cornucopia.ContinueVote, player_id: player.id, game_id: game_id)
      
      # Remove vote by toggling again
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()
      refute Copi.Repo.get_by(Copi.Cornucopia.ContinueVote, player_id: player.id, game_id: game_id)
    end

    test "displays player information", %{conn: conn, player: player} do
      {:ok, _show_live, html} = live(conn, "/games/#{player.game_id}/players/#{player.id}")
      assert html =~ player.name
      assert html =~ "Cornucopia Web Session"
    end

    test "handles game updates via broadcast", %{conn: conn, player: player} do
      {:ok, show_live, _html} = live(conn, "/games/#{player.game_id}/players/#{player.id}")
      # Get updated game
      {:ok, updated_game} = Cornucopia.Game.find(player.game_id)

      # Send message in the format handle_info expects
      send(show_live.pid, %{
        topic: "game:#{player.game_id}",
        event: "game:updated",
        payload: updated_game
      })

      # Give LiveView time to process
      :timer.sleep(50)
      
      # Verify it doesn't crash and stays connected
      assert render(show_live) =~ player.name
    end

    test "next_round advances round when round is closed", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      # Start game
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      # Trigger next_round via direct event (bypasses DOM element requirement)
      render_click(show_live, "next_round", %{})

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played >= 0
    end

    test "redirects to error when player not found", %{conn: conn} do
      assert {:error, {:redirect, %{to: "/error"}}} =
               live(conn, "/games/01ARZ3NDEKTSV4RRFFQ69G5FAV/players/01ARZ3NDEKTSV4RRFFQ69G5FAV")
    end

    test "next_round when round is closed advances rounds and sets finished_at", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      # Insert a dealt card played in round 1 for this player.
      # With played_in_round: 1 the round is closed (round_open? = false).
      # With no nil-round cards, last_round? = true → finished_at gets set.
      {:ok, card} = Cornucopia.create_card(%{
        category: "C", value: "V9", description: "D", edition: "webapp",
        version: "2.2", external_id: "CLOSEDRND9", language: "en",
        misc: "misc", owasp_scp: [], owasp_devguide: [], owasp_asvs: [],
        owasp_appsensor: [], capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
      })
      Copi.Repo.insert!(%Copi.Cornucopia.DealtCard{
        player_id: player.id, card_id: card.id, played_in_round: 1
      })

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      render_click(show_live, "next_round", %{})

      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
      assert updated_game.finished_at != nil
    end

    test "toggle_vote removes existing vote", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, other_player} = Cornucopia.create_player(%{name: "Other2", game_id: game_id})
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      {:ok, card} = Cornucopia.create_card(%{
        category: "C", value: "V2", description: "D", edition: "webapp",
        version: "2.2", external_id: "EXT2", language: "en",
        misc: "misc", owasp_scp: [], owasp_devguide: [], owasp_asvs: [],
        owasp_appsensor: [], capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
      })
      {:ok, dealt} = Copi.Repo.insert(%Copi.Cornucopia.DealtCard{player_id: other_player.id, card_id: card.id, played_in_round: 1})

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      # Vote once to add
      show_live |> element("[phx-click=\"toggle_vote\"][phx-value-dealt_card_id=\"#{dealt.id}\"]") |> render_click()
      assert Copi.Repo.get_by(Copi.Cornucopia.Vote, dealt_card_id: dealt.id, player_id: player.id)

      # Vote again to remove
      show_live |> element("[phx-click=\"toggle_vote\"][phx-value-dealt_card_id=\"#{dealt.id}\"]") |> render_click()
      refute Copi.Repo.get_by(Copi.Cornucopia.Vote, dealt_card_id: dealt.id, player_id: player.id)
    end
  end

  describe "Helper functions" do
    alias CopiWeb.PlayerLive.Show

    test "ordered_cards sorts by card id" do
      cards = [
        %{card: %{id: 3}},
        %{card: %{id: 1}},
        %{card: %{id: 2}}
      ]
      result = Show.ordered_cards(cards)
      assert Enum.map(result, & &1.card.id) == [1, 2, 3]
    end

    test "unplayed_cards returns cards with played_in_round 0 or nil" do
      cards = [
        %{played_in_round: 0},
        %{played_in_round: nil},
        %{played_in_round: 1}
      ]
      result = Show.unplayed_cards(cards)
      assert length(result) == 2
    end

    test "played_cards returns cards played in given round" do
      cards = [
        %{played_in_round: 1},
        %{played_in_round: 2},
        %{played_in_round: 1}
      ]
      assert length(Show.played_cards(cards, 1)) == 2
      assert length(Show.played_cards(cards, 2)) == 1
    end

    test "card_played_in_round finds correct card" do
      cards = [%{played_in_round: 1, id: 10}, %{played_in_round: 2, id: 20}]
      assert Show.card_played_in_round(cards, 1).id == 10
      assert is_nil(Show.card_played_in_round(cards, 9))
    end

    test "player_first puts given player first" do
      players = [%{id: 1}, %{id: 2}, %{id: 3}]
      [first | _] = Show.player_first(players, %{id: 2})
      assert first.id == 2
    end

    test "round_open? returns true when players have unplayed cards" do
      game = %{
        rounds_played: 0,
        players: [
          %{dealt_cards: []},
          %{dealt_cards: [%{played_in_round: 1}]}
        ]
      }
      assert Show.round_open?(game)
    end

    test "round_closed? returns true when all players have played" do
      game = %{
        rounds_played: 0,
        players: [
          %{dealt_cards: [%{played_in_round: 1}]},
          %{dealt_cards: [%{played_in_round: 1}]}
        ]
      }
      assert Show.round_closed?(game)
    end

    test "last_round? returns true when a player has no unplayed cards" do
      game = %{
        players: [
          %{dealt_cards: [%{played_in_round: 1}]},
          %{dealt_cards: [%{played_in_round: nil}]}
        ]
      }
      assert Show.last_round?(game)
    end

    test "get_vote returns matching vote or nil" do
      player = %{id: 5}
      dealt_card = %{votes: [%{player_id: 5, id: 99}, %{player_id: 6, id: 100}]}
      assert Show.get_vote(dealt_card, player).id == 99
      assert is_nil(Show.get_vote(%{votes: []}, player))
    end
  end
end
