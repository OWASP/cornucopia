defmodule CopiWeb.GameLiveTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia
  alias Copi.RateLimiter

  @create_attrs %{ name: "some name", edition: "webapp"}
  # @update_attrs %{ name: "some updated name", edition: "webapp"}
  @invalid_attrs %{name: nil, edition: "webapp"}

  setup %{conn: conn} do
    # Clear rate limits to prevent cross-test contamination
    RateLimiter.clear_ip({127, 0, 0, 1})
    # Set up IP address for rate limiting tests
    conn = Plug.Conn.put_private(conn, :connect_info, %{peer_data: %{address: {127, 0, 0, 1}}})
    {:ok, conn: conn}
  end

  defp fixture(:game) do
    {:ok, game} = Cornucopia.create_game(@create_attrs)
    game
  end

  defp create_game(_) do
    game = fixture(:game)
    %{game: game}
  end

  describe "Index" do
    setup [:create_game]

    test "List the new game", %{conn: conn, game: game} do
      {:ok, _index_game, html} = live(conn, "/games/#{game.id}")

      assert html =~ "some name"
    end

    test "saves new game", %{conn: conn} do
      {:ok, index_live, _html} = live(conn, "/games")
      {:ok, new_conn} = index_live |> element(~s{[href="/games/new"]}) |> render_click() |> follow_redirect(conn)
      assert_redirect(index_live, Routes.game_index_path(conn, :new))


      {:ok, games_new, html_games_new} = live(new_conn, "/games/new")

      assert html_games_new =~ "Start A Game"

      assert games_new
             |> form("#game-form", game: @invalid_attrs)
             |> render_change() =~ "No really, give your game session a name"

      {:ok, _, html} =
        games_new
        |> form("#game-form", game: @create_attrs)
        |> render_submit()
        |> follow_redirect(conn)

      assert html =~ "Game created successfully"
      assert html =~ "some name"
    end

    test "blocks game creation when rate limit exceeded", %{conn: conn} do
      # Clear any existing rate limits for the test IP
      test_ip = {127, 0, 0, 1}
      RateLimiter.clear_ip(test_ip)

      # Get the rate limit config
      config = RateLimiter.get_config()
      limit = config.limits.game_creation

      # Navigate to new game page once and reuse the LiveView
      {:ok, index_live, _html} = live(conn, "/games")
      {:ok, _} = index_live |> element(~s{[href="/games/new"]}) |> render_click() |> follow_redirect(conn)
      
      # Create games up to the limit
      for i <- 1..limit do
        {:ok, games_new, _html} = live(conn, "/games/new")
        
        {:ok, _, _html} =
          games_new
          |> form("#game-form", game: %{name: "Game #{i}", edition: "webapp"})
          |> render_submit()
          |> follow_redirect(conn)
      end

      # Next game creation should be blocked
      {:ok, games_new_blocked, _html} = live(conn, "/games/new")
      
      games_new_blocked
        |> form("#game-form", game: %{name: "Blocked Game", edition: "webapp"})
        |> render_submit()
      
      # Verify rate limit is exceeded (form stays, no redirect)
      assert has_element?(games_new_blocked, "#game-form")
      # Verify the rate limiter actually blocked the request
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate({127, 0, 0, 1}, :game_creation)
    end
  end

  describe "Show" do
    setup [:create_game]

    test "displays game", %{conn: conn, game: game} do
      {:ok, _show_live, html} = live(conn, Routes.game_show_path(conn, :show, game))

      assert html =~ "Waiting for players to join the game..."
      assert html =~ game.name
      refute html =~ "Start Game"
    end

    test "starts game when enough players", %{conn: conn, game: game} do
      # Create 3 players
      {:ok, _} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P2", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P3", game_id: game.id})



      {:ok, show_live, html} = live(conn, Routes.game_show_path(conn, :show, game))
      assert html =~ "Start Game"

      html = show_live |> element("button[phx-click=\"start_game\"]") |> render_click()
      assert html =~ "Round <strong>1</strong>"
    end
    
    test "Broadcasts game:updated to other LiveViews but ignores non-matching topic", %{conn: conn, game: game} do
      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")
      
      # Should be ignored due to topic mismatch, no crash
      send(show_live.pid, %{topic: "game:other_id", event: "game:updated", payload: game})
      assert render(show_live) =~ game.name
    end

    test "redirects to error when game not found", %{conn: conn} do
      assert {:error, {:redirect, %{to: "/error"}}} = live(conn, "/games/01ARZ3NDEKTSV4RRFFQ69G5FAV")
    end

    test "displays finished game using rounds_played for current_round", %{conn: conn, game: game} do
      # Set finished_at so handle_params uses game.rounds_played (not +1) for current_round
      {:ok, game} = Cornucopia.update_game(game, %{
        started_at: DateTime.truncate(DateTime.utc_now(), :second),
        finished_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 1
      })
      {:ok, _show_live, html} = live(conn, Routes.game_show_path(conn, :show, game))
      assert html =~ game.name
    end

    test "displays past round", %{conn: conn, game: game} do
       # Create players and play a round to make it valid
       {:ok, p1} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
       {:ok, card} = Cornucopia.create_card(%{
        category: "C", value: "V", description: "D", edition: "webapp",
        version: "2.2", external_id: "EXT", language: "en",
        misc: "misc", owasp_scp: [], owasp_devguide: [], owasp_asvs: [],
        owasp_appsensor: [], capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
      })
      {:ok, _} = Copi.Repo.insert(%Copi.Cornucopia.DealtCard{player_id: p1.id, card_id: card.id, played_in_round: 1})
      
       # Advance game to round 2 and set started_at
       {:ok, game} = Cornucopia.update_game(game, %{rounds_played: 1, started_at: DateTime.from_naive!(~N[2023-01-01 10:00:00], "Etc/UTC")})
       
       {:ok, _show_live, html} = live(conn, "/games/#{game.id}?round=1")
       assert html =~ "Viewing round <strong>1</strong>"
    end


    test "handle_info updates games list", %{conn: conn} do
      {:ok, index_live, _html} = live(conn, "/games")
      
      # Send update_parent message
      send(index_live.pid, {:update_parent, []})
      
      # Should update the assigns
      :ok
    end

    test "start_game does nothing when game already started", %{conn: conn, game: game} do
      # Pre-start the game with 3 players
      {:ok, _} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P2", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P3", game_id: game.id})
      {:ok, game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})

      {:ok, show_live, _html} = live(conn, Routes.game_show_path(conn, :show, game))

      # Clicking start_game on an already started game should be a noop
      html = render(show_live)
      refute html =~ "Start Game"
    end

    test "start_game shows error flash with fewer than 3 players", %{conn: conn, game: game} do
      # Only 2 players — below minimum
      {:ok, _} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P2", game_id: game.id})

      {:ok, show_live, _html} = live(conn, Routes.game_show_path(conn, :show, game))

      render_click(show_live, "start_game", %{})
      html = render(show_live)
      assert html =~ "At least 3 players are required"
    end

    test "redirects to error on invalid round param", %{conn: conn, game: game} do
      {:ok, _} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
      {:ok, game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})

      # round=999 is way beyond current_round, should redirect to /error
      assert {:error, {:redirect, %{to: "/error"}}} = live(conn, "/games/#{game.id}?round=999")
    end
  end

  describe "Helper functions" do
    alias CopiWeb.GameLive.Show

    test "display_game_session returns correct label for each edition" do
      assert Show.display_game_session("webapp") =~ "Cornucopia Web Session"
      assert Show.display_game_session("ecommerce") =~ "Cornucopia Web Session"
      assert Show.display_game_session("mobileapp") =~ "Cornucopia Mobile Session"
      assert Show.display_game_session("mlsec") =~ "Elevation of MLSec Session"
      assert Show.display_game_session("cumulus") =~ "OWASP Cumulus Session"
      assert Show.display_game_session("masvs") =~ "Cornucopia Mobile Session"
      assert Show.display_game_session("eop") =~ "EoP Session"
      assert Show.display_game_session("unknown") =~ "EoP Session"
    end

    test "latest_version returns correct version for each edition" do
      assert Show.latest_version("webapp") == "2.2"
      assert Show.latest_version("ecommerce") == "1.22"
      assert Show.latest_version("mobileapp") == "1.1"
      assert Show.latest_version("mlsec") == "1.0"
      assert Show.latest_version("cumulus") == "1.1"
      assert Show.latest_version("masvs") == "1.1"
      assert Show.latest_version("eop") == "5.1"
      assert Show.latest_version("other") == "1.0"
    end

    test "card_played_in_round returns correct card" do
      cards = [
        %{played_in_round: 1, id: 1},
        %{played_in_round: 2, id: 2},
        %{played_in_round: nil, id: 3}
      ]
      assert Show.card_played_in_round(cards, 1).id == 1
      assert Show.card_played_in_round(cards, 2).id == 2
      assert is_nil(Show.card_played_in_round(cards, 3))
    end
  end
end
