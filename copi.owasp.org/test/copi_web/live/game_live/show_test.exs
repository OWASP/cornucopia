defmodule CopiWeb.GameLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia

  @game_attrs %{name: "Edge Case Test Game", edition: "webapp", suits: ["hearts", "clubs"]}

  defp create_game(_) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    %{game: game}
  end

  describe "Show - Edge Cases" do
    setup [:create_game]

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
  end
end
