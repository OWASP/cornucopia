defmodule CopiWeb.GameLive.Index do
  use CopiWeb, :live_view
  use Phoenix.Component

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    {:ok, assign(assign(socket, :client_ip, ip), :games, nil)}
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :new, _params) do
    socket
    |> assign(:page_title, "Create a new game")
    |> assign(:game, %Game{})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Games")
    |> assign(:game, nil)
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    game = Cornucopia.get_game!(id)
    {:ok, _} = Cornucopia.delete_game(game)

    {:noreply, assign(socket, :games, nil)}
  end

  defp list_games do
    Cornucopia.list_games()
  end

  @impl true
  def handle_info({:update_parent, new_state}, socket) do
    {:noreply, assign(socket, :games, new_state)}
  end

end
