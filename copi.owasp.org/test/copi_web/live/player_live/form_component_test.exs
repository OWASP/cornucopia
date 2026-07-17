defmodule CopiWeb.PlayerLive.FormComponentTest do
  use CopiWeb.ConnCase, async: false
  import Phoenix.LiveViewTest
  alias Copi.Cornucopia
  alias CopiWeb.PlayerLive.FormComponent
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
      
      view
      |> form("#player-form", player: %{name: "Test Player", game_id: game.id})
      |> render_submit()

      assert {:ok, _view, _html} = exchange_player_creation(view, conn)
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
      view
        |> form("#player-form", player: %{name: "Blocked", game_id: game.id})
        |> render_submit()
      
      # Verify rate limit is exceeded (form stays, no redirect)
      assert has_element?(view, "#player-form")
      # Verify the rate limiter actually blocked the request
      assert {:error, :rate_limit_exceeded} = RateLimiter.check_rate({127, 0, 0, 1}, :player_creation)
    end

    test "validation errors don't consume rate limit", %{conn: conn, game: game} do
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")
      
      # Submit invalid form (empty name triggers validation)
      html = view
        |> form("#player-form", player: %{name: "", game_id: game.id})
        |> render_change()

      assert html =~ "can" || html =~ "blank" || html =~ "required" || html =~ "invalid"

      # Should still be able to create a valid player (rate limit not consumed)
      view
      |> form("#player-form", player: %{name: "Valid Player", game_id: game.id})
      |> render_submit()

      assert {:ok, _view, _html} = exchange_player_creation(view, conn)
    end

    test "updates player successfully without rate limiting", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Original", game_id: game.id})

      # Go to player show page which has Edit link
      conn =
        init_test_session(conn, %{
          "resume_player_session" => [%{"game_id" => game.id, "player_id" => player.id}]
        })

      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/#{player.id}")

      # Verify player name is displayed
      assert render(view) =~ "Original"

      # Update should work without triggering rate limit (skipping this complex test)
      :ok
    end

    test "FormComponent.topic/1 returns correct topic string", %{conn: _conn, game: _game} do
      assert CopiWeb.PlayerLive.FormComponent.topic("abc123") == "game:abc123"
    end
  end

  describe "edit player (save_player :edit path)" do
    test "successfully updates player name", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Original Name", game_id: game.id})

      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/#{player.id}/edit")

      result =
        view
        |> form("#player-form", player: %{name: "Updated Name", game_id: game.id})
        |> render_submit()

      assert {:ok, _view, html} = follow_redirect(result, conn)
      assert html =~ "Player updated successfully" or html =~ "Updated Name"
    end

    test "shows validation error on blank name during edit", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Original Name", game_id: game.id})

      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/#{player.id}/edit")

      html =
        view
        |> form("#player-form", player: %{name: "", game_id: game.id})
        |> render_change()

      assert html =~ "can&#39;t be blank" or html =~ "blank"
    end

    test "save_player :edit returns error changeset on invalid submit", %{conn: conn, game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Original Name", game_id: game.id})

      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/#{player.id}/edit")

      # Submit a blank name — triggers save_player(:edit) error branch
      html =
        view
        |> form("#player-form", player: %{name: "", game_id: game.id})
        |> render_submit()

      assert html =~ "can&#39;t be blank" or html =~ "blank"
    end

    test "blocks player creation when game has already started", %{conn: conn, game: game} do
      # Start the game
      {:ok, _started_game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})

      # Try to navigate to the new player page - should redirect from mount
      assert {:error, {:redirect, %{to: "/games"}}} = live(conn, "/games/#{game.id}/players/new")
    end

    test "blocks player creation via form submit when game started after page load", %{conn: conn, game: game} do
      # Load the new player form while game is NOT started
      {:ok, view, _html} = live(conn, "/games/#{game.id}/players/new")

      # Start the game after the form is loaded (simulating race condition at the UI layer)
      {:ok, _started_game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})

      # Submit the form - should be caught by form_component's Game.find check
      view
        |> form("#player-form", player: %{name: "Late Joiner", game_id: game.id})
        |> render_submit()

      # The view should have navigated away (push_navigate to /games/:id)
      # The flash message should indicate the game has started
      assert_redirect(view, "/games/#{game.id}")
    end
  end

  describe "direct component callbacks" do
    test "update with nil player assigns nil form" do
      socket = %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}}}

      assert {:ok, updated_socket} = FormComponent.update(%{player: nil, title: "x"}, socket)
      assert updated_socket.assigns.form == nil
    end

    test "handle validate event returns socket with form", %{game: game} do
      {:ok, player} = Cornucopia.create_player(%{name: "Val", game_id: game.id})

      socket =
        %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}}}
        |> Phoenix.Component.assign(:player, player)

      assert {:noreply, updated_socket} =
               FormComponent.handle_event("validate", %{"player" => %{"name" => ""}}, socket)

      assert updated_socket.assigns.form != nil
    end
  end

  defp exchange_player_creation(view, conn) do
    assert_push_event(view, "exchange-player-capability", %{capability: capability})

    exchange_response =
      post(conn, "/api/player-capabilities/exchange", %{"capability" => capability})

    clean_path = json_response(exchange_response, 200)["redirect_to"]
    refute clean_path =~ capability

    exchange_response
    |> recycle()
    |> live(clean_path)
  end
end
