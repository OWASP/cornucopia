defmodule CopiWeb.PlayerLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Player
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end

  @impl true
  def handle_params(%{"id" => player_id}, _, socket) do
    with {:ok, player} <- Player.find(player_id) do
      with {:ok, game} <- Game.find(player.game_id) do
        CopiWeb.Endpoint.subscribe(topic(player.game_id))
        {:noreply, socket |> assign(:page_title, page_title(socket.assigns.live_action)) |> assign(:game, game) |> assign(:player, player)}
      else
        {:error, _reason} ->
          {:ok, redirect(socket, to: "/error")}
      end
    else
      {:error, _reason} ->
        {:ok, redirect(socket, to: "/error")}
    end
  end

  @impl true
  def handle_info(%{topic: message_topic, event: "game:updated", payload: game}, socket) do
    cond do
      topic(game.id) == message_topic ->
        {:noreply, socket |> assign(:game, Copi.Repo.preload(game, players: :dealt_cards))}
      true ->
        {:noreply, socket}
    end
  end

  defp page_title(:show), do: "Show Player"
  defp page_title(:edit), do: "Edit Player"

  def format_capec(refs) do
    refs
    |> Enum.map(fn ref -> link(ref, to: "https://capec.mitre.org/data/definitions/#{ref}.html") end)
    |> Enum.intersperse(", ")
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
