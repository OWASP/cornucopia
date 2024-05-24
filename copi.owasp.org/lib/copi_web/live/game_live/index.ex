defmodule CopiWeb.GameLive.Index do
  use CopiWeb, :live_view
  use Phoenix.Component
  import CopiWeb.LiveHelpers

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :games, nil)}
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

    {:noreply, assign(socket, :games, list_games())}
  end

  defp list_games do
    Cornucopia.list_games()
  end
end
