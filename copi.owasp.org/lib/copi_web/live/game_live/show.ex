defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end

  @impl true
  def handle_params(%{"id" => game_id}, _, socket) do
    with {:ok, game} <- Game.find(game_id) do
      CopiWeb.Endpoint.subscribe(topic(game_id))
      {:noreply, socket |> assign(:game, game)}
    else
      {:error, _reason} ->
        {:ok, redirect(socket, to: "/error")}
    end
  end

  @impl true
  def handle_info(%{topic: message_topic, event: "game:updated", payload: game}, socket) do
    cond do
      topic(game.id) == message_topic ->
        {:noreply, assign(socket, :game, Copi.Repo.preload(game, players: :dealt_cards))}
      true ->
        {:noreply, socket}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
