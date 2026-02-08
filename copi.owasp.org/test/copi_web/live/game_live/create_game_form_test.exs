defmodule CopiWeb.GameLive.CreateGameFormTest do
  use CopiWeb.ConnCase, async: false
  import Phoenix.LiveViewTest
  alias Copi.RateLimiter

  setup %{conn: conn} do
    test_ip = {127, 0, 0, 1}
    RateLimiter.clear_ip(test_ip)
    # Set up IP address for rate limiting tests
    conn = Plug.Conn.put_private(conn, :connect_info, %{peer_data: %{address: test_ip}})
    {:ok, conn: conn, ip: test_ip}
  end

  describe "rate limiting in game creation" do
    test "allows game creation under limit", %{conn: conn} do
      {:ok, view, _html} = live(conn, "/games/new")
      
      html = view
        |> form("#game-form", game: %{name: "Test Game", edition: "webapp"})
        |> render_submit()

      assert html =~ "Game created successfully"
    end

    test "shows error message when limit exceeded", %{conn: conn, ip: _ip} do
      config = RateLimiter.get_config()
      limit = config.limits.game_creation

      # Create games up to the limit
      for i <- 1..limit do
        {:ok, view, _html} = live(conn, "/games/new")
        view
          |> form("#game-form", game: %{name: "Game #{i}", edition: "webapp"})
          |> render_submit()
      end

      # Next attempt should be blocked
      {:ok, view, _html} = live(conn, "/games/new")
      html = view
        |> form("#game-form", game: %{name: "Blocked", edition: "webapp"})
        |> render_submit()

      assert html =~ "Too many game creation attempts"
    end

    test "validation errors don't consume rate limit", %{conn: conn} do
      {:ok, view, _html} = live(conn, "/games/new")
      
      # Submit invalid form
      html = view
        |> form("#game-form", game: %{name: nil, edition: "webapp"})
        |> render_change()

      assert html =~ "can&#39;t be blank"

      # Should still be able to create a valid game
      html = view
        |> form("#game-form", game: %{name: "Valid Game", edition: "webapp"})
        |> render_submit()

      assert html =~ "Game created successfully"
    end
  end
end
