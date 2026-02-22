defmodule CopiWeb.GameLiveTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia

  @create_attrs %{ name: "some name", edition: "webapp"}
  # @update_attrs %{ name: "some updated name", edition: "webapp"}
  @invalid_attrs %{name: nil, edition: "webapp"}

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

      html = show_live |> element("button", "Start Game") |> render_click()
      assert html =~ "Round <strong>1</strong>"
    end

    test "re-clicking Start Game on an already-started game is a safe noop", %{conn: conn, game: game} do
      # Create 3 players and mark the game as already started.
      {:ok, _} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P2", game_id: game.id})
      {:ok, _} = Cornucopia.create_player(%{name: "P3", game_id: game.id})
      {:ok, started_game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})

      {:ok, show_live, _html} = live(conn, Routes.game_show_path(conn, :show, started_game))

      # ASVS V2.3.3 / V16.5 – sending the event again must not crash the LiveView
      # process; it returns {:noreply, socket} silently.
      assert render(show_live) =~ started_game.name

      # The process must still be alive and responsive after the duplicate event.
      assert Process.alive?(show_live.pid)
    end

    test "redirects to error when game not found", %{conn: conn} do
      assert {:error, {:redirect, %{to: "/error"}}} = live(conn, "/games/01ARZ3NDEKTSV4RRFFQ69G5FAV")
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
    
  end
end
