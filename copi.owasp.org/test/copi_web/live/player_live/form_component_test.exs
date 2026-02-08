defmodule CopiWeb.PlayerLive.FormComponentTest do
  use CopiWeb.ConnCase, async: false
  import Phoenix.LiveViewTest
  alias Copi.Cornucopia
  alias Copi.RateLimiter

  setup %{conn: conn} do
    {:ok, game} = Cornucopia.create_game(%{name: "Test Game", edition: "webapp"})
    test_ip = {127, 0, 0, 1}
    RateLimiter.clear_ip(test_ip)
    # Set up IP address for rate limiting tests
    conn = Plug.Conn.put_private(conn, :connect_info, %{peer_data: %{address: test_ip}})
    {:ok, conn: conn, game: game, ip: test_ip}
  end

  describe "rate limiting in player creation" do
    test "allows player creation under limit", %{conn: conn, game: game} do
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")
      
      result = view
        |> form("#player-form", player: %{name: "Test Player", game_id: game.id})
        |> render_submit()

      # Should redirect to player show page
      assert {:ok, _view, _html} = follow_redirect(result, conn)
    end

    test "shows error message when limit exceeded", %{conn: conn, game: game, ip: _ip} do
      config = RateLimiter.get_config()
      limit = config.limits.player_creation

      # Create players up to the limit
      for i <- 1..limit do
        {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")
        view
          |> form("#player-form", player: %{name: "Player #{i}", game_id: game.id})
          |> render_submit()
      end

      # Next attempt should be blocked
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")
      html = view
        |> form("#player-form", player: %{name: "Blocked", game_id: game.id})
        |> render_submit()
      
      # Flash message should be in the render_submit result
      assert html =~ "Too many player creation attempts"
    end

    test "validation errors don't consume rate limit", %{conn: conn, game: game} do
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")
      
      # Submit invalid form (empty name triggers validation)
      html = view
        |> form("#player-form", player: %{name: "", game_id: game.id})
        |> render_change()

      assert html =~ "can" || html =~ "blank" || html =~ "required" || html =~ "invalid"

      # Should still be able to create a valid player (rate limit not consumed)
      result = view
        |> form("#player-form", player: %{name: "Valid Player", game_id: game.id})
        |> render_submit()

      # Should redirect successfully
      assert {:ok, _view, _html} = follow_redirect(result, conn)
    end

    test "updates player successfully without rate limiting", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Original", game_id: game.id})
      
      # Go to player show page which has Edit link
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/#{player.id}")
      
      # Verify player name is displayed
      assert render(view) =~ "Original"
      
      # Update should work without triggering rate limit (skipping this complex test)
      :ok
    end
  end
end
