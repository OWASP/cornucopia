defmodule CopiWeb.PlayerLive.Index do
  use CopiWeb, :live_view

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Player

  @impl true
  def mount(%{"game_id" => game_id}, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    {:ok, assign(assign(socket, :client_ip, ip), players: Cornucopia.list_players(game_id), game: Cornucopia.get_game!(game_id))}
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
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

end
