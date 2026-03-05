defmodule CopiWeb.PlayerLive.Index do
  use CopiWeb, :live_view

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Player

  @impl true
  def mount(%{"game_id" => game_id}, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    game = Cornucopia.get_game!(game_id)

    # V2.2: Block at mount — returning redirect from mount sends a true HTTP 302
    # during the dead (static) render, before any HTML or WebSocket reaches the client.
    if not is_nil(game.started_at) do
      {:ok,
       socket
       |> put_flash(:error, "This game has already started. New players cannot join a game in progress.")
       |> redirect(to: ~p"/games")}
    else
      {:ok, assign(assign(socket, :client_ip, ip), players: list_players(game_id), game: game)}
    end
  end

  @impl true
  def handle_params(%{"game_id" => game_id} = params, _url, socket) do
    # Re-fetch game state for LiveView client-side navigations (when mount isn't called)
    game = Cornucopia.get_game!(game_id)

    # V2.2: Also check in handle_params for LiveView navigation scenarios
    if not is_nil(game.started_at) do
      {:noreply,
       socket
       |> put_flash(:error, "This game has already started. New players cannot join a game in progress.")
       |> redirect(to: ~p"/games")}
    else
      {:noreply, apply_action(socket, socket.assigns.live_action, params)}
    end
  end

  defp apply_action(socket, :edit, %{"id" => id}) do
    socket
    |> assign(:page_title, "Edit Player")
    |> assign(:player, Cornucopia.get_player!(id))
  end

  defp apply_action(socket, :new, %{"game_id" => game_id}) do
    game = socket.assigns.game
    socket
    |> assign(:page_title, "You're joining the game: #{game.name}")
    |> assign(:player, %Player{game_id: game_id})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Players")
    |> assign(:player, nil)
  end

  defp list_players(game_id) do
    Cornucopia.list_players(game_id)
  end
end
