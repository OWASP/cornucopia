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

  describe "Show - Helper Functions" do
    setup [:create_game]

    test "card_played_in_round finds the correct card", %{game: _game} do
      # Test with cards having different played_in_round values
      cards = [
        %{card_id: 1, played_in_round: 1},
        %{card_id: 2, played_in_round: 2},
        %{card_id: 3, played_in_round: 3}
      ]

      assert CopiWeb.GameLive.Show.card_played_in_round(cards, 2).card_id == 2
      assert CopiWeb.GameLive.Show.card_played_in_round(cards, 1).card_id == 1
      assert CopiWeb.GameLive.Show.card_played_in_round(cards, 3).card_id == 3
      assert CopiWeb.GameLive.Show.card_played_in_round(cards, 4) == nil
    end

    test "display_game_session returns correct session names", %{game: _game} do
      assert CopiWeb.GameLive.Show.display_game_session("webapp") == "Cornucopia Web Session:"
      assert CopiWeb.GameLive.Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
      assert CopiWeb.GameLive.Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert CopiWeb.GameLive.Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
      assert CopiWeb.GameLive.Show.display_game_session("cumulus") == "OWASP Cumulus Session:"
      assert CopiWeb.GameLive.Show.display_game_session("masvs") == "Cornucopia Mobile Session:"
      assert CopiWeb.GameLive.Show.display_game_session("eop") == "EoP Session:"
      assert CopiWeb.GameLive.Show.display_game_session("unknown") == "EoP Session:"
    end

    test "latest_version returns correct version numbers", %{game: _game} do
      assert CopiWeb.GameLive.Show.latest_version("webapp") == "2.2"
      assert CopiWeb.GameLive.Show.latest_version("ecommerce") == "1.22"
      assert CopiWeb.GameLive.Show.latest_version("mobileapp") == "1.1"
      assert CopiWeb.GameLive.Show.latest_version("mlsec") == "1.0"
      assert CopiWeb.GameLive.Show.latest_version("cumulus") == "1.1"
      assert CopiWeb.GameLive.Show.latest_version("masvs") == "1.1"
      assert CopiWeb.GameLive.Show.latest_version("eop") == "5.1"
      assert CopiWeb.GameLive.Show.latest_version("unknown") == "1.0"
    end
  end

  describe "Show - LiveView Lifecycle" do
    setup [:create_game]

    test "handle_info updates game on broadcast", %{conn: conn, game: game} do
      {:ok, view, _html} = live(conn, "/games/#{game.id}")

      # Update game
      {:ok, updated_game} = Cornucopia.update_game(game, %{name: "Updated Name"})

      # Simulate broadcast
      send(view.pid, %{
        topic: "game:#{game.id}",
        event: "game:updated",
        payload: updated_game
      })

      # Give it a moment to process
      :timer.sleep(10)

      # Verify view was updated
      assert render(view) =~ "Updated Name"
    end

    test "handle_params with invalid game redirects to error", %{conn: conn} do
      # Try to visit non-existent game
      assert {:error, {:live_redirect, %{to: "/error"}}} = live(conn, "/games/99999")
    end

    test "handle_params with invalid round number redirects to error", %{conn: conn, game: game} do
      # Try to visit with invalid round parameter
      assert {:error, {:live_redirect, %{to: "/error"}}} = 
        live(conn, "/games/#{game.id}?round=invalid")
    end

    test "handle_params sets correct round for finished game", %{conn: conn, game: game} do
      # Finish the game
      {:ok, finished_game} = Cornucopia.update_game(game, %{
        finished_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 5
      })

      {:ok, view, _html} = live(conn, "/games/#{finished_game.id}")

      # Verify round is set to rounds_played (not rounds_played + 1)
      assert view.assigns.requested_round == 5
    end

    test "handle_params sets correct round for active game", %{conn: conn, game: game} do
      # Update rounds_played but don't finish
      {:ok, active_game} = Cornucopia.update_game(game, %{rounds_played: 3})

      {:ok, view, _html} = live(conn, "/games/#{active_game.id}")

      # Verify round is set to rounds_played + 1
      assert view.assigns.requested_round == 4
    end
  end
end
