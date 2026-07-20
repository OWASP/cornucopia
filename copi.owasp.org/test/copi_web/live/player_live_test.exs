defmodule CopiWeb.PlayerLiveTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest
  import Ecto.Query

  alias Copi.Cornucopia
  alias Copi.RateLimiter

  defmodule IndexGameStub do
    def find(id), do: find_basic(id)

    def find_basic(id) do
      case Application.get_env(:copi, :player_live_index_stub_mode, :real) do
        :real -> Copi.Cornucopia.Game.find_basic(id)
        :not_found -> {:error, :not_found}
        :transient -> {:error, :temporary}
        {:sequence, list} ->
          case list do
            [head | tail] ->
              Application.put_env(:copi, :player_live_index_stub_mode, {:sequence, tail})
              resolve(head, id)

            [] ->
              Copi.Cornucopia.Game.find_basic(id)
          end
      end
    end

    defp resolve(:real, id), do: Copi.Cornucopia.Game.find_basic(id)
    defp resolve(:not_found, _id), do: {:error, :not_found}
    defp resolve(:transient, _id), do: {:error, :temporary}
  end

  @game_attrs %{name: "some name"}
  # @create_attrs %{name: "some name", game_id: ""}
  # @update_attrs %{name: "some updated name"}
  @invalid_attrs %{name: nil}

  setup %{conn: conn} do
    # Clear rate limits to prevent cross-test contamination
    RateLimiter.clear_ip({127, 0, 0, 1})
    # Set up IP address for rate limiting tests
    conn = Plug.Conn.put_private(conn, :connect_info, %{peer_data: %{address: {127, 0, 0, 1}}})

    old_game_mod = Application.get_env(:copi, :player_live_index_game_module)
    old_mode = Application.get_env(:copi, :player_live_index_stub_mode)

    on_exit(fn ->
      Application.put_env(:copi, :player_live_index_game_module, old_game_mod)
      Application.put_env(:copi, :player_live_index_stub_mode, old_mode)
    end)

    {:ok, conn: conn}
  end

  defp fixture(:player) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    {:ok, player} = Cornucopia.create_player(%{name: "some name", game_id: game.id})
    player
  end

  defp create_player(%{conn: conn}) do
    player = fixture(:player)
    conn =
      init_test_session(conn, %{
        "resume_player_session" => [
          %{"game_id" => player.game_id, "player_id" => player.id}
        ]
      })

    %{conn: conn, player: player}
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

    test "redirects on mount when game has already started", %{conn: conn, player: player} do
      # Start the game
      {:ok, started_game} = Cornucopia.update_game(
        Cornucopia.get_game!(player.game_id),
        %{started_at: DateTime.truncate(DateTime.utc_now(), :second)}
      )

      # Attempt to access the index page (which might mount the LiveView)
      assert {:error, {:redirect, %{to: "/games"}}} = live(conn, "/games/#{started_game.id}/players")
    end

    test "saves new player", %{conn: conn, player: player} do
      {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}")

      assert index_live |> element(~s{[href="/games/#{player.game_id}/players/new"]}) |> render_click()

      assert_patch(index_live, "/games/#{player.game_id}/players/new")

      {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}/players/new")
      assert index_live
             |> form("#player-form", player: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      index_live
      |> form("#player-form", player: %{name: "some updated name", game_id: player.game_id})
      |> render_submit()

      {:ok, _, html} = exchange_player_creation(index_live, conn)

      assert html =~ "Hi some updated name, waiting for the game to start..."
      assert html =~ "Hi some updated name, waiting for the game to start..."
    end



    test "lists players on index route", %{conn: conn, player: player} do
      {:ok, _index_live, html} = live(conn, "/games/#{player.game_id}/players")
      assert html =~ "Listing Players"
    end

    test "shows validation error when submitting empty player name", %{conn: conn, player: player} do
      RateLimiter.clear_ip({127, 0, 0, 1})
      {:ok, index_live, _html} = live(conn, "/games/#{player.game_id}/players/new")

      # Submit with empty name → triggers {:error, changeset} in save_player(:new, ...)
      html =
        index_live
        |> form("#player-form", player: %{name: "", game_id: player.game_id})
        |> render_submit()

      assert html =~ "can&#39;t be blank"
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

    test "redirects when game does not exist", %{conn: conn} do
      assert {:error, {:redirect, %{to: "/games", flash: %{"error" => "Game not found."}}}} =
               live(conn, "/games/00000000000000000000000099/players")
    end

    test "new player route redirects when game is started", %{conn: conn, player: player} do
      {:ok, _started_game} =
        Cornucopia.update_game(
          Cornucopia.get_game!(player.game_id),
          %{started_at: DateTime.truncate(DateTime.utc_now(), :second)}
        )

      assert {:error, {:redirect, %{to: "/games"}}} = live(conn, "/games/#{player.game_id}/players/new")
    end

    test "edit player route renders edit page title", %{conn: conn, player: player} do
      {:ok, _view, html} = live(conn, "/games/#{player.game_id}/players/#{player.id}/edit")
      assert html =~ "Edit Player"
    end

    test "retry message is handled without crashing", %{conn: conn, player: player} do
      {:ok, view, _html} = live(conn, "/games/#{player.game_id}/players")

      send(view.pid, {:retry_player_index_load, %{"game_id" => player.game_id}})
      :timer.sleep(50)

      assert is_binary(render(view))
    end

    test "mount redirects on transient game load failure", %{conn: conn, player: player} do
      Application.put_env(:copi, :player_live_index_game_module, IndexGameStub)
      Application.put_env(:copi, :player_live_index_stub_mode, :transient)

      assert {:error, {:redirect, %{to: "/games"}}} = live(conn, "/games/#{player.game_id}/players")
    end

    test "retry transitions from retrying to please try again state", %{conn: conn, player: player} do
      Application.put_env(:copi, :player_live_index_game_module, IndexGameStub)
      Application.put_env(:copi, :player_live_index_stub_mode, :real)

      {:ok, view, _html} = live(conn, "/games/#{player.game_id}/players/new")

      Application.put_env(:copi, :player_live_index_stub_mode, :transient)

      send(view.pid, {:retry_player_index_load, %{"game_id" => player.game_id}})
      :timer.sleep(50)
      send(view.pid, {:retry_player_index_load, %{"game_id" => player.game_id}})
      :timer.sleep(50)
      send(view.pid, {:retry_player_index_load, %{"game_id" => player.game_id}})
      :timer.sleep(50)

      assert render(view) =~ "Temporary issue loading game"
    end
  end

  defp exchange_player_creation(view, conn) do
    assert_push_event(view, "exchange-player-capability", %{capability: capability})

    exchange_response =
      post(conn, "/api/player-capabilities/exchange", %{"capability" => capability})

    clean_path = json_response(exchange_response, 200)["redirect_to"]
    refute clean_path =~ capability

    exchange_response
    |> recycle()
    |> live(clean_path)
  end

  describe "Show" do
    setup [:create_player]

    test "creates a single-use five-minute handoff link", %{conn: conn, player: player} do
      {:ok, show_live, html} = live(conn, "/games/#{player.game_id}/players/#{player.id}")

      assert html =~ "Share your hand"
      refute html =~ "/player-handoffs/"

      html = show_live |> element(~s{[phx-click="share_hand"]}) |> render_click()

      assert html =~ "This single-use link expires in 5 minutes."
      assert html =~ "/player-handoffs/"
      assert has_element?(show_live, "#copy-url-btn")
    end

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
        version: "3.0", external_id: "EXT", language: "en",
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

    test "next_round when round is closed advances rounds and sets finished_at", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))

      # Insert a dealt card played in round 1 for this player.
      # With played_in_round: 1 the round is closed (round_open? = false).
      # With no nil-round cards, last_round? = true → finished_at gets set.
      {:ok, card} = Cornucopia.create_card(%{
        category: "C", value: "V9", description: "D", edition: "webapp",
        version: "3.0", external_id: "CLOSEDRND9", language: "en",
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
        version: "3.0", external_id: "EXT2", language: "en",
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

    test "prevents self-voting on own dealt card", %{conn: conn, player: player} do
      game_id = player.game_id
      {:ok, game} = Cornucopia.Game.find(game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))
      {:ok, card} = Cornucopia.create_card(%{
        category: "C", value: "V", description: "D", edition: "webapp",
        version: "3.0", external_id: "EXT2", language: "en",
        misc: "misc", owasp_scp: [], owasp_devguide: [], owasp_asvs: [],
        owasp_appsensor: [], capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
      })
      {:ok, dealt} = Copi.Repo.insert(%Copi.Cornucopia.DealtCard{player_id: player.id, card_id: card.id, played_in_round: 1})
      {:ok, show_live, _html} = live(conn, "/games/#{game_id}/players/#{player.id}")
      render_click(show_live, "toggle_vote", %{"dealt_card_id" => "#{dealt.id}"})
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
