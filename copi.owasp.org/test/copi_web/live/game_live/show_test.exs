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
      {:ok, player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, player3} = Cornucopia.create_player(%{name: "Player 3", game_id: game.id})

      {:ok, view, html} = live(conn, "/games/#{game.id}")
      
      # Button should be visible with 3+ players
      assert html =~ "Start Game"

      # Start game
      view |> element("button", "Start Game") |> render_click()

      # Verify game was started
      {:ok, updated_game} = Cornucopia.Game.find(game.id)
      assert updated_game.started_at != nil
      
      # Verify cards were dealt to all players via transaction
      player1_cards = Cornucopia.list_player_cards(player1.id)
      player2_cards = Cornucopia.list_player_cards(player2.id)
      player3_cards = Cornucopia.list_player_cards(player3.id)
      
      # Each player should have cards
      assert length(player1_cards) > 0
      assert length(player2_cards) > 0
      assert length(player3_cards) > 0
      
      # Total cards should equal 52 (standard deck) distributed evenly
      total_cards = length(player1_cards) + length(player2_cards) + length(player3_cards)
      assert total_cards == 52
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

    test "transaction ensures atomic card dealing with 4 players", %{conn: conn, game: game} do
      # Add 4 players to test round-robin distribution
      {:ok, player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, player3} = Cornucopia.create_player(%{name: "Player 3", game_id: game.id})
      {:ok, player4} = Cornucopia.create_player(%{name: "Player 4", game_id: game.id})

      {:ok, view, _html} = live(conn, "/games/#{game.id}")

      # Start game
      render_click(view, "start_game", %{})

      # Verify game started
      {:ok, updated_game} = Cornucopia.Game.find(game.id)
      assert updated_game.started_at != nil

      # Verify all 52 cards were dealt atomically
      player1_cards = Cornucopia.list_player_cards(player1.id)
      player2_cards = Cornucopia.list_player_cards(player2.id)
      player3_cards = Cornucopia.list_player_cards(player3.id)
      player4_cards = Cornucopia.list_player_cards(player4.id)

      # Each player should get 13 cards (52 / 4)
      assert length(player1_cards) == 13
      assert length(player2_cards) == 13
      assert length(player3_cards) == 13
      assert length(player4_cards) == 13

      # Verify game update broadcast happened (started_at is set)
      assert updated_game.started_at != nil
    end

    test "transaction with 5 players distributes cards evenly", %{conn: conn, game: game} do
      # Add 5 players
      {:ok, player1} = Cornucopia.create_player(%{name: "Player 1", game_id: game.id})
      {:ok, player2} = Cornucopia.create_player(%{name: "Player 2", game_id: game.id})
      {:ok, player3} = Cornucopia.create_player(%{name: "Player 3", game_id: game.id})
      {:ok, player4} = Cornucopia.create_player(%{name: "Player 4", game_id: game.id})
      {:ok, player5} = Cornucopia.create_player(%{name: "Player 5", game_id: game.id})

      {:ok, view, _html} = live(conn, "/games/#{game.id}")
      render_click(view, "start_game", %{})

      # Verify cards distributed via transaction
      player1_cards = Cornucopia.list_player_cards(player1.id)
      player2_cards = Cornucopia.list_player_cards(player2.id)
      player3_cards = Cornucopia.list_player_cards(player3.id)
      player4_cards = Cornucopia.list_player_cards(player4.id)
      player5_cards = Cornucopia.list_player_cards(player5.id)

      # With 5 players, first 2 players get 11 cards, last 3 get 10 (52 cards total)
      total = length(player1_cards) + length(player2_cards) + length(player3_cards) + 
              length(player4_cards) + length(player5_cards)
      assert total == 52
      
      # All players should have at least 10 cards
      assert length(player1_cards) >= 10
      assert length(player2_cards) >= 10
      assert length(player3_cards) >= 10
      assert length(player4_cards) >= 10
      assert length(player5_cards) >= 10
    end
  end
end
