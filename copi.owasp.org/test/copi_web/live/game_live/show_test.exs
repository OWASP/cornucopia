defmodule CopiWeb.GameLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia

  defmodule GameStub do
    def find(id) do
      case Application.get_env(:copi, :game_live_show_stub_mode, :real) do
        :real -> Copi.Cornucopia.Game.find(id)
        :not_found -> {:error, :not_found}
        :transient -> {:error, :temporary}
        {:sequence, list} ->
          case list do
            [head | tail] ->
              Application.put_env(:copi, :game_live_show_stub_mode, {:sequence, tail})
              resolve(head, id)

            [] ->
              Copi.Cornucopia.Game.find(id)
          end
      end
    end

    defp resolve(:real, id), do: Copi.Cornucopia.Game.find(id)
    defp resolve(:not_found, _id), do: {:error, :not_found}
    defp resolve(:transient, _id), do: {:error, :temporary}
  end

  @game_attrs %{name: "Edge Case Test Game", edition: "webapp", suits: ["hearts", "clubs"]}

  defp create_game(_) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    %{game: game}
  end

  describe "Show - Edge Cases" do
    setup [:create_game]

    setup do
      old_game_mod = Application.get_env(:copi, :game_live_show_game_module)
      old_mode = Application.get_env(:copi, :game_live_show_stub_mode)

      on_exit(fn ->
        Application.put_env(:copi, :game_live_show_game_module, old_game_mod)
        Application.put_env(:copi, :game_live_show_stub_mode, old_mode)
      end)

      :ok
    end

    test "prevents starting game with fewer than 3 players", %{conn: conn, game: game} do
      # Test with 0 players
      {:ok, view, html} = live(conn, "/games/#{game.id}")
      refute html =~ "Start Game"
      
      # Directly trigger start_game event to test server-side validation
      render_click(view, "start_game", %{})
      assert render(view) =~ "At least 3 players are required"
      
      {:ok, updated_game} = Cornucopia.Game.find(game.id)
      assert updated_game.started_at == nil

      # Test with 1 player
      {:ok, _player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, view, html} = live(conn, "/games/#{game.id}")
      refute html =~ "Start Game"
      
      render_click(view, "start_game", %{})
      assert render(view) =~ "At least 3 players are required"

      # Test with 2 players
      {:ok, _player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, view, html} = live(conn, "/games/#{game.id}")
      refute html =~ "Start Game"
      
      render_click(view, "start_game", %{})
      assert render(view) =~ "At least 3 players are required"
    end

    test "successfully starts game with 3+ players", %{conn: conn, game: game} do
      # Add 3 players
      {:ok, _player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, _player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, _player3} = Cornucopia.create_player(%{name: "Player 3", game_id: game.id})

      {:ok, view, html} = live(conn, "/games/#{game.id}")
      
      # Button should be visible with 3+ players
      assert html =~ "Start Game"

      # Start game
      view |> element("button", "Start Game") |> render_click()

      # Verify game was started
      {:ok, updated_game} = Cornucopia.Game.find(game.id)
      assert updated_game.started_at != nil
    end

    test "start_game deals cards when deck has cards", %{conn: conn, game: game} do
      {:ok, _player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, _player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, _player3} = Cornucopia.create_player(%{name: "Player 3", game_id: game.id})

      for i <- 1..3 do
        {:ok, _card} =
          Cornucopia.create_card(%{
            category: if(rem(i, 2) == 0, do: "clubs", else: "hearts"),
            value: "V#{i}",
            description: "D",
            edition: "webapp",
            version: "3.0",
            external_id: "GS#{i}",
            language: "en",
            misc: "m",
            owasp_scp: [],
            owasp_devguide: [],
            owasp_asvs: [],
            owasp_appsensor: [],
            capec: [],
            safecode: [],
            owasp_mastg: [],
            owasp_masvs: []
          })
      end

      {:ok, view, _html} = live(conn, "/games/#{game.id}")
      view |> element("button", "Start Game") |> render_click()

      {:ok, started_game} = Cornucopia.Game.find(game.id)
      dealt_count =
        started_game.players
        |> Enum.flat_map(& &1.dealt_cards)
        |> Enum.count()

      assert dealt_count > 0
    end

    test "does not restart an already started game", %{conn: conn, game: game} do
      # Add 3 players
      {:ok, _player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, _player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, _player3} = Cornucopia.create_player(%{name: "Player 3", game_id: game.id})

      # Start game first
      {:ok, started_game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})
      original_time = started_game.started_at

      {:ok, view, html} = live(conn, "/games/#{started_game.id}")

      # Button should not be visible after game has started
      refute html =~ "Start Game"

      # Try to start again via direct event trigger - should do nothing
      render_click(view, "start_game", %{})

      # Verify started_at timestamp hasn't changed
      {:ok, updated_game} = Cornucopia.Game.find(started_game.id)
      assert DateTime.compare(updated_game.started_at, original_time) == :eq
    end

    test "handle_info updates game when matching topic received", %{conn: conn, game: game} do
      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")

      {:ok, updated_game} = Cornucopia.Game.find(game.id)

      send(show_live.pid, %{
        topic: "game:#{game.id}",
        event: "game:updated",
        payload: updated_game
      })

      :timer.sleep(50)
      assert render(show_live) =~ game.name
    end

    test "display_game_session/1 returns correct label for each edition", %{conn: _conn, game: _game} do
      alias CopiWeb.GameLive.Show
      assert Show.display_game_session("webapp")    == "Cornucopia Web Session:"
      assert Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("masvs")     == "Cornucopia Mobile Session:"
      assert Show.display_game_session("mlsec")     == "Elevation of MLSec Session:"
      assert Show.display_game_session("cumulus")   == "OWASP Cumulus Session:"
      assert Show.display_game_session("eop")       == "EoP Session:"
    end

    test "latest_version/1 returns correct version string for each edition", %{conn: _conn, game: _game} do
      alias CopiWeb.GameLive.Show
      assert Show.latest_version("webapp")    == "3.0"
      assert Show.latest_version("ecommerce") == "1.22"
      assert Show.latest_version("mobileapp") == "1.1"
      assert Show.latest_version("mlsec")     == "1.0"
      assert Show.latest_version("cumulus")   == "1.1"
      assert Show.latest_version("masvs")     == "1.1"
      assert Show.latest_version("eop")       == "5.1"
      assert Show.latest_version("unknown")   == "1.0"
    end

    test "card_played_in_round/2 returns nil when no card matches", %{conn: _conn, game: _game} do
      alias CopiWeb.GameLive.Show
      assert Show.card_played_in_round([], 1) == nil
    end

    test "card_played_in_round/2 returns the matching card", %{conn: _conn, game: _game} do
      alias CopiWeb.GameLive.Show

      cards = [%{played_in_round: 1, id: "a"}, %{played_in_round: 2, id: "b"}]
      assert Show.card_played_in_round(cards, 2) == %{played_in_round: 2, id: "b"}
    end

    test "topic/1 builds topic strings", %{conn: _conn, game: _game} do
      alias CopiWeb.GameLive.Show
      assert Show.topic(1) == "game:1"
      assert Show.topic("xyz") == "game:xyz"
    end

    test "handle_info ignores update for a different game id", %{conn: conn, game: game} do
      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")

      {:ok, other_game} = Copi.Cornucopia.create_game(%{name: "other"})
      {:ok, other_game_loaded} = Copi.Cornucopia.Game.find(other_game.id)

      send(show_live.pid, %{
        topic: "game:#{game.id}",
        event: "game:updated",
        payload: other_game_loaded
      })

      :timer.sleep(50)
      assert render(show_live) =~ game.name
    end

    test "handle_params uses rounds_played directly for finished game", %{conn: conn, game: game} do
      {:ok, finished_game} =
        Cornucopia.update_game(game, %{
          started_at: DateTime.truncate(DateTime.utc_now(), :second),
          finished_at: DateTime.truncate(DateTime.utc_now(), :second),
          rounds_played: 2
        })

      {:ok, _view, html} = live(conn, "/games/#{finished_game.id}")
      assert html =~ finished_game.name
    end

    test "shows a resume player link when the encrypted session points at this game", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Player Resume", game_id: game.id})

      conn =
        conn
        |> init_test_session(%{"resume_player_session" => %{"game_id" => game.id, "player_id" => player.id}})

      {:ok, _view, html} = live(conn, "/games/#{game.id}")

      assert html =~ "Resume your player session from this browser session."
      assert html =~ "/games/#{game.id}/players/#{player.id}"
    end

    test "handle_info with non-matching topic is no-op", %{conn: conn, game: game} do
      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")
      {:ok, updated_game} = Cornucopia.Game.find(game.id)

      send(show_live.pid, %{
        topic: "game:completely-different-id",
        event: "game:updated",
        payload: updated_game
      })

      :timer.sleep(50)
      assert render(show_live) =~ game.name
    end

    test "retry handle_info does not crash and keeps view active", %{conn: conn, game: game} do
      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")

      send(show_live.pid, {:retry_game_load, %{"game_id" => game.id}})
      :timer.sleep(50)

      assert render(show_live) =~ game.name
    end

    test "redirects to /games when game does not exist", %{conn: conn} do
      assert {:error, {:redirect, %{to: "/games", flash: %{"error" => "Game not found."}}}} =
               live(conn, "/games/00000000000000000000000099")
    end

    test "redirects to /games on transient load when no previous game assign", %{conn: conn, game: game} do
      Application.put_env(:copi, :game_live_show_game_module, GameStub)
      Application.put_env(:copi, :game_live_show_stub_mode, :transient)

      assert {:error, {:redirect, %{to: "/games"}}} = live(conn, "/games/#{game.id}")
    end

    test "retry flow increments counter then stops retrying", %{conn: conn, game: game} do
      Application.put_env(:copi, :game_live_show_game_module, GameStub)
      Application.put_env(:copi, :game_live_show_stub_mode, :real)

      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")

      Application.put_env(:copi, :game_live_show_stub_mode, :transient)

      send(show_live.pid, {:retry_game_load, %{"game_id" => game.id}})
      :timer.sleep(50)
      send(show_live.pid, {:retry_game_load, %{"game_id" => game.id}})
      :timer.sleep(50)
      send(show_live.pid, {:retry_game_load, %{"game_id" => game.id}})
      :timer.sleep(50)

      assert render(show_live) =~ "Temporary issue loading game"
    end

    test "invalid round value falls back to current round and stays on page", %{conn: conn, game: game} do
      {:ok, _view, html} = live(conn, "/games/#{game.id}?round=999")
      assert html =~ game.name
      assert html =~ "Invalid round value. Showing current round instead."
    end
  end
end
