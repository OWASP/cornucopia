defmodule CopiWeb.GameLive.ShowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia
  alias CopiWeb.GameLive.Show

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
      {:ok, started_game} =
        Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})

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

    test "handle_info ignores game:updated events for a different game", %{conn: conn, game: game} do
      {:ok, show_live, _html} = live(conn, "/games/#{game.id}")
      {:ok, other_game} = Cornucopia.create_game(%{name: "Other Game", edition: "webapp"})

      # Send a broadcast whose topic doesn't match what show.ex subscribed to,
      # so the `true ->` branch in the cond fires and socket is returned unchanged
      send(show_live.pid, %{
        topic: "game:mismatch-id",
        event: "game:updated",
        payload: other_game
      })

      :timer.sleep(50)
      assert render(show_live) =~ game.name
    end
  end

  describe "Show helper functions" do
    test "topic returns expected pubsub topic" do
      assert Show.topic("abc123") == "game:abc123"
    end

    test "card_played_in_round finds a card in requested round" do
      cards = [
        %{played_in_round: 1, card: %{id: 1}},
        %{played_in_round: 2, card: %{id: 2}}
      ]

      assert Show.card_played_in_round(cards, 2) == %{played_in_round: 2, card: %{id: 2}}
      assert Show.card_played_in_round(cards, 3) == nil
    end

    test "display_game_session returns labels for known and unknown editions" do
      assert Show.display_game_session("webapp") == "Cornucopia Web Session:"
      assert Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("masvs") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("cumulus") == "OWASP Cumulus Session:"
      assert Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
      assert Show.display_game_session("eop") == "EoP Session:"
      assert Show.display_game_session("unknown") == "EoP Session:"
    end

    test "latest_version returns expected version by edition" do
      assert Show.latest_version("webapp") == "2.2"
      assert Show.latest_version("ecommerce") == "1.22"
      assert Show.latest_version("mobileapp") == "1.1"
      assert Show.latest_version("mlsec") == "1.0"
      assert Show.latest_version("cumulus") == "1.1"
      assert Show.latest_version("masvs") == "1.1"
      assert Show.latest_version("eop") == "5.1"
      assert Show.latest_version("unknown") == "1.0"
    end

    test "put_uri_hook stores uri in socket assigns" do
      socket = %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}}}

      assert {:cont, updated_socket} = Show.put_uri_hook(%{}, "/games/round/1", socket)
      assert updated_socket.assigns.uri == "/games/round/1"
    end

  end
end
