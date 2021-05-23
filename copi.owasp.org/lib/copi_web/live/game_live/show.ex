defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end

  @impl true
  def handle_params(%{"id" => id}, _, socket) do
    with {:ok, game} <- Game.find(id) do
      {:noreply, socket |> assign(:game, game)}
    else
      {:error, _reason} ->
        {:ok, redirect(socket, to: "/error")}
    end
  end

end
