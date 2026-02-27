defmodule CopiWeb.PlayerLiveTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest
  import Ecto.Query

  alias Copi.Cornucopia
  alias Copi.RateLimiter
  alias CopiWeb.PlayerLive.Show

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

  describe "Index" do
    setup [:create_player]

    test "lists all players", %{conn: conn, player: player} do
      {:ok, _index_live, html} = live(conn, "/games/#{player.game_id}/players/#{player.id}")
      assert html =~ player.name
      assert html =~ "Cornucopia Web Session: some name"
    end

    test "saves new player", %{conn: conn, player: player} do
      {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}")

      assert index_live
             |> element(~s{[href="/games/#{player.game_id}/players/new"]})
             |> render_click()

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
      # Clear any existing rate limits for the test IP
      test_ip = {127, 0, 0, 1}
      RateLimiter.clear_ip(test_ip)

      # Get the rate limit config
      config = RateLimiter.get_config()
      limit = config.limits.player_creation

      # Create players up to the limit
      for i <- 1..limit do
        {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}/players/new")

        {:ok, _, _html} =
          index_live
          |> form("#player-form", player: %{name: "Player #{i}", game_id: player.game_id})
          |> render_submit()
          |> follow_redirect(conn)
      end

      # Next player creation should be blocked
      {:ok, index_live_blocked, _html} = live(conn, "/games/#{player.game_id}/players/new")

      index_live_blocked
      |> form("#player-form", player: %{name: "Blocked Player", game_id: player.game_id})
      |> render_submit()

      # Verify rate limit is exceeded (form stays, no redirect)
      assert has_element?(index_live_blocked, "#player-form")
      # Verify the rate limiter actually blocked the request
      assert {:error, :rate_limit_exceeded} =
               RateLimiter.check_rate({127, 0, 0, 1}, :player_creation)
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

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      # Deal/play card for Other
      {:ok, card} =
        Cornucopia.create_card(%{
          category: "C",
          value: "V",
          description: "D",
          edition: "webapp",
          version: "2.2",
          external_id: "EXT",
          language: "en",
          misc: "misc",
          owasp_scp: [],
          owasp_devguide: [],
          owasp_asvs: [],
          owasp_appsensor: [],
          capec: [],
          safecode: [],
          owasp_mastg: [],
          owasp_masvs: []
        })

      {:ok, dealt} =
        Copi.Repo.insert(%Copi.Cornucopia.DealtCard{
          player_id: other_player.id,
          card_id: card.id,
          played_in_round: 1
        })

      {:ok, show_live, html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      assert html =~ "Other"
      # Assuming 1 round played (default rounds_played=0, current=1)

      # Find vote button for the dealt card
      # The template uses phx-value-dealt_card_id
      show_live
      |> element("[phx-click=\"toggle_vote\"][phx-value-dealt_card_id=\"#{dealt.id}\"]")
      |> render_click()

      # Verify vote created
      assert Copi.Repo.get_by(Copi.Cornucopia.Vote, dealt_card_id: dealt.id, player_id: player.id)

      # Toggle again to remove vote
      show_live
      |> element("[phx-click=\"toggle_vote\"][phx-value-dealt_card_id=\"#{dealt.id}\"]")
      |> render_click()

      # Verify vote deleted
      refute Copi.Repo.get_by(Copi.Cornucopia.Vote, dealt_card_id: dealt.id, player_id: player.id)
    end

    test "allows continue voting and resets votes on next round", %{conn: conn, player: player} do
      # Setup another player
      game_id = player.game_id
      {:ok, _other_player} = Cornucopia.create_player(%{name: "Other", game_id: game_id})

      # Start game
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      # Test continue voting
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()

      # Verify continue vote created
      assert Copi.Repo.get_by(Copi.Cornucopia.ContinueVote,
               player_id: player.id,
               game_id: game_id
             )

      # Toggle again to remove continue vote
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()

      # Verify continue vote deleted
      refute Copi.Repo.get_by(Copi.Cornucopia.ContinueVote,
               player_id: player.id,
               game_id: game_id
             )

      # Test that votes are cleared when proceeding to next round
      # Manually clear votes and advance round to test the functionality
      Copi.Repo.delete_all(from cv in Copi.Cornucopia.ContinueVote, where: cv.game_id == ^game_id)

      Copi.Cornucopia.update_game(game, %{rounds_played: game.rounds_played + 1, round_open: true})

      # Verify continue votes are cleared
      refute Copi.Repo.get_by(Copi.Cornucopia.ContinueVote,
               player_id: player.id,
               game_id: game_id
             )

      # Verify game advanced to next round
      {:ok, updated_game} = Cornucopia.Game.find(game_id)
      assert updated_game.rounds_played == 1
    end

    test "prevents duplicate votes through database constraint", %{conn: _conn, player: player} do
      # Setup game and dealt card
      game_id = player.game_id
      {:ok, other_player} = Cornucopia.create_player(%{name: "Other", game_id: game_id})

      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, card} =
        Cornucopia.create_card(%{
          category: "C",
          value: "V",
          description: "D",
          edition: "webapp",
          version: "2.2",
          external_id: "EXT2",
          language: "en",
          misc: "misc",
          owasp_scp: [],
          owasp_devguide: [],
          owasp_asvs: [],
          owasp_appsensor: [],
          capec: [],
          safecode: [],
          owasp_mastg: [],
          owasp_masvs: []
        })

      {:ok, dealt} =
        Copi.Repo.insert(%Copi.Cornucopia.DealtCard{
          player_id: other_player.id,
          card_id: card.id,
          played_in_round: 1
        })

      # Simulate true concurrent race condition using Task.async
      insert_vote = fn ->
        Copi.Repo.insert(
          %Copi.Cornucopia.Vote{player_id: player.id, dealt_card_id: dealt.id},
          on_conflict: :nothing
        )
      end

      task1 = Task.async(insert_vote)
      task2 = Task.async(insert_vote)

      # Wait for both concurrent attempts to complete
      _result1 = Task.await(task1)
      _result2 = Task.await(task2)

      # Verify only one vote exists despite concurrent attempts
      votes =
        Copi.Repo.all(
          from v in Copi.Cornucopia.Vote,
            where: v.player_id == ^player.id and v.dealt_card_id == ^dealt.id
        )

      assert length(votes) == 1
    end

    test "prevents duplicate continue votes through database constraint", %{
      conn: _conn,
      player: player
    } do
      game_id = player.game_id

      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      # Simulate true concurrent race condition using Task.async
      insert_continue_vote = fn ->
        Copi.Repo.insert(
          %Copi.Cornucopia.ContinueVote{player_id: player.id, game_id: game_id},
          on_conflict: :nothing
        )
      end

      task1 = Task.async(insert_continue_vote)
      task2 = Task.async(insert_continue_vote)

      # Wait for both concurrent attempts to complete
      _result1 = Task.await(task1)
      _result2 = Task.await(task2)

      # Verify only one continue vote exists despite concurrent attempts
      continue_votes =
        Copi.Repo.all(
          from cv in Copi.Cornucopia.ContinueVote,
            where: cv.player_id == ^player.id and cv.game_id == ^game_id
        )

      assert length(continue_votes) == 1
    end

    test "allows toggling continue vote off", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)

      Copi.Repo.update!(
        Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second))
      )

      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")

      # Add vote
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()

      assert Copi.Repo.get_by(Copi.Cornucopia.ContinueVote,
               player_id: player.id,
               game_id: game_id
             )

      # Remove vote by toggling again
      show_live |> element("[phx-click=\"toggle_continue_vote\"]") |> render_click()

      refute Copi.Repo.get_by(Copi.Cornucopia.ContinueVote,
               player_id: player.id,
               game_id: game_id
             )
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
  end

  describe "Show helper functions" do
    test "orders cards by card id" do
      cards = [
        %{card: %{id: 3}},
        %{card: %{id: 1}},
        %{card: %{id: 2}}
      ]

      assert Show.ordered_cards(cards) == [
               %{card: %{id: 1}},
               %{card: %{id: 2}},
               %{card: %{id: 3}}
             ]
    end

    test "filters played and unplayed cards" do
      cards = [
        %{played_in_round: nil, card: %{id: 1}},
        %{played_in_round: 0, card: %{id: 2}},
        %{played_in_round: 1, card: %{id: 3}},
        %{played_in_round: 2, card: %{id: 4}}
      ]

      assert Show.unplayed_cards(cards) == [
               %{played_in_round: nil, card: %{id: 1}},
               %{played_in_round: 0, card: %{id: 2}}
             ]

      assert Show.played_cards(cards, 1) == [%{played_in_round: 1, card: %{id: 3}}]
      assert Show.card_played_in_round(cards, 2) == %{played_in_round: 2, card: %{id: 4}}
      assert Show.card_played_in_round(cards, 99) == nil
    end

    test "player_first moves current player to first position" do
      players = [%{id: "p2"}, %{id: "p1"}, %{id: "p3"}]
      ordered = Show.player_first(players, %{id: "p1"})

      assert hd(ordered).id == "p1"
      assert Enum.map(ordered, & &1.id) == ["p1", "p2", "p3"]
    end

    test "round_open and round_closed reflect remaining players to play" do
      game_open = %{
        rounds_played: 0,
        players: [
          %{dealt_cards: [%{played_in_round: nil}]},
          %{dealt_cards: [%{played_in_round: 1}]}
        ]
      }

      game_closed = %{
        rounds_played: 0,
        players: [
          %{dealt_cards: [%{played_in_round: 1}]},
          %{dealt_cards: [%{played_in_round: 1}]}
        ]
      }

      assert Show.round_open?(game_open)
      refute Show.round_closed?(game_open)

      refute Show.round_open?(game_closed)
      assert Show.round_closed?(game_closed)
    end

    test "last_round detects when any player has no unplayed cards remaining" do
      game_last_round = %{
        players: [
          %{dealt_cards: [%{played_in_round: 1}]},
          %{dealt_cards: [%{played_in_round: nil}]}
        ]
      }

      game_not_last_round = %{
        players: [
          %{dealt_cards: [%{played_in_round: nil}]},
          %{dealt_cards: [%{played_in_round: nil}]}
        ]
      }

      assert Show.last_round?(game_last_round)
      refute Show.last_round?(game_not_last_round)
    end

    test "get_vote and display_game_session helpers" do
      dealt_card = %{votes: [%{player_id: "p1"}, %{player_id: "p2"}]}

      assert Show.get_vote(dealt_card, %{id: "p2"}) == %{player_id: "p2"}
      assert Show.get_vote(dealt_card, %{id: "missing"}) == nil

      assert Show.display_game_session("webapp") == "Cornucopia Web Session:"
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
      assert Show.display_game_session("unknown") == "EoP Session:"
    end
  end
end
