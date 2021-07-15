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
        {:noreply, socket |> assign(:game, game) |> assign(:player, player)}
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
  def handle_info(%{topic: _message_topic, event: "game:updated", payload: _game}, socket) do
    with {:ok, updated_player} <- Player.find(socket.assigns.player.id) do
      with {:ok, updated_game} <- Game.find(updated_player.game_id) do
        {:noreply, socket |> assign(:game, updated_game) |> assign(:player, updated_player)}
      else
        {:error, _reason} ->
          {:ok, redirect(socket, to: "/error")}
      end
    else
      {:error, _reason} ->
        {:ok, redirect(socket, to: "/error")}
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

  def ordered_cards(cards) do
    Enum.sort_by(cards, &(&1.card.id))
  end

  def unplayed_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round in [0, nil] end)
  end

  def played_cards(cards, round) do
    Enum.filter(cards, fn card -> card.played_in_round == round end)
  end

  def card_played_in_round(cards, round) do
    dealt_card = Enum.find(cards, fn card -> card.played_in_round == round end)

    if dealt_card, do: dealt_card.card, else: nil
  end
end
