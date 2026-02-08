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
      
      _html = view
        |> form("#player-form", player: %{name: "Test Player", game_id: game.id})
        |> render_submit()

      # Should redirect to player page
      assert_redirect(view, ~r"/games/.*/players/.*")
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

      assert html =~ "Too many player creation attempts"
    end

    test "validation errors don't consume rate limit", %{conn: conn, game: game} do
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")
      
      # Submit invalid form
      html = view
        |> form("#player-form", player: %{name: nil, game_id: game.id})
        |> render_change()

      assert html =~ "can&#39;t be blank"

      # Should still be able to create a valid player
      view
        |> form("#player-form", player: %{name: "Valid Player", game_id: game.id})
        |> render_submit()

      # Should redirect successfully
      assert_redirect(view, ~r"/games/.*/players/.*")
    end

    test "updates player successfully without rate limiting", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Original", game_id: game.id})
      
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/#{player.id}/edit")
      
      _result = view
        |> form("#player-form", player: %{name: "Updated Name"})
        |> render_submit()

      # Update should redirect successfully
      assert_redirect(view, ~r"/games/.*/players/.*")
    end
  end
end
