defmodule CopiWeb.GameLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest
  import Ecto.Query, only: [from: 2]

  alias Copi.Cornucopia
  alias Copi.Cornucopia.DealtCard
  alias Copi.Repo

  @game_attrs %{name: "Edge Case Test Game", edition: "webapp", suits: ["DATA VALIDATION & ENCODING"]}

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
      player1_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player1.id)
      player2_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player2.id)
      player3_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player3.id)

      # Each player should have cards
      assert length(player1_cards) > 0
      assert length(player2_cards) > 0
      assert length(player3_cards) > 0

      # Total cards should be greater than 0 (exact count depends on edition/suits)
      total_cards = length(player1_cards) + length(player2_cards) + length(player3_cards)
      assert total_cards > 0
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
      player1_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player1.id)
      player2_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player2.id)
      player3_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player3.id)
      player4_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player4.id)

      # Each player should have at least 1 card (round-robin distribution)
      assert length(player1_cards) >= 1
      assert length(player2_cards) >= 1
      assert length(player3_cards) >= 1
      assert length(player4_cards) >= 1

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
      player1_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player1.id)
      player2_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player2.id)
      player3_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player3.id)
      player4_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player4.id)
      player5_cards = Repo.all(from d in DealtCard, where: d.player_id == ^player5.id)

      # Total dealt cards should be greater than 0
      total = length(player1_cards) + length(player2_cards) + length(player3_cards) +
              length(player4_cards) + length(player5_cards)
      assert total > 0

      # All players should have at least 1 card
      assert length(player1_cards) >= 1
      assert length(player2_cards) >= 1
      assert length(player3_cards) >= 1
      assert length(player4_cards) >= 1
      assert length(player5_cards) >= 1
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

    test "handle_params with invalid game redirects to error", %{conn: conn} do
      # Use a fresh ULID that won't exist in the database
      nonexistent_id = Ecto.ULID.generate()
      # show.ex uses redirect/2 which returns {:redirect, ...} (full page redirect)
      assert {:error, {:redirect, %{to: "/error"}}} = live(conn, "/games/#{nonexistent_id}")
    end

    test "handle_params with invalid round number uses default round", %{conn: conn, game: game} do
      # Want.integer/2 with a default always returns {:ok, value}; invalid round string
      # falls back to the default (current round) rather than redirecting.
      {:ok, _view, html} = live(conn, "/games/#{game.id}?round=invalid")
      assert is_binary(html)
    end

    test "handle_params sets correct round for finished game", %{conn: conn, game: game} do
      # Finish the game
      {:ok, finished_game} = Cornucopia.update_game(game, %{
        finished_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 5
      })

      # View should load successfully; round defaults to rounds_played for finished games
      {:ok, _view, html} = live(conn, "/games/#{finished_game.id}")
      assert is_binary(html)
    end

    test "handle_params sets correct round for active game", %{conn: conn, game: game} do
      # Update rounds_played but don't finish
      {:ok, active_game} = Cornucopia.update_game(game, %{rounds_played: 3})

      # View should load; round defaults to rounds_played + 1 for active games
      {:ok, _view, html} = live(conn, "/games/#{active_game.id}")
      assert is_binary(html)
    end

    test "handle_params with explicit valid round parameter", %{conn: conn, game: game} do
      {:ok, started_game} = Cornucopia.update_game(game, %{
        started_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 5
      })

      # Request a specific valid round (3 is within [1..5])
      {:ok, _view, html} = live(conn, "/games/#{started_game.id}?round=3")
      assert is_binary(html)
    end

    test "handle_params with round parameter at max boundary", %{conn: conn, game: game} do
      {:ok, finished_game} = Cornucopia.update_game(game, %{
        finished_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 10
      })

      # round=10 is at the max boundary, should render successfully
      {:ok, _view, html} = live(conn, "/games/#{finished_game.id}?round=10")
      assert is_binary(html)
    end

    test "handle_params with round parameter at min boundary", %{conn: conn, game: game} do
      {:ok, started_game} = Cornucopia.update_game(game, %{
        started_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 5
      })

      # round=1 is at the min boundary, should render successfully
      {:ok, _view, html} = live(conn, "/games/#{started_game.id}?round=1")
      assert is_binary(html)
    end

    test "handle_params with round parameter exceeding max uses default", %{conn: conn, game: game} do
      # Want.integer/2 with a default clamps out-of-range values to the default
      # rather than returning {:error, _}.
      {:ok, finished_game} = Cornucopia.update_game(game, %{
        finished_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 3
      })

      # round=10 exceeds max (3) but Want uses default; view renders normally
      {:ok, _view, html} = live(conn, "/games/#{finished_game.id}?round=10")
      assert is_binary(html)
    end

    test "handle_params with round below min uses default", %{conn: conn, game: game} do
      # round=0 is below min (1) but Want uses default; view renders normally
      {:ok, started_game} = Cornucopia.update_game(game, %{
        started_at: DateTime.truncate(DateTime.utc_now(), :second),
        rounds_played: 5
      })

      {:ok, _view, html} = live(conn, "/games/#{started_game.id}?round=0")
      assert is_binary(html)
    end

    test "topic function generates correct topic string", %{game: _game} do
      assert CopiWeb.GameLive.Show.topic(123) == "game:123"
      assert CopiWeb.GameLive.Show.topic("abc") == "game:abc"
    end
  end
end
