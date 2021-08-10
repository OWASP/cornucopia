defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.DealtCard

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end

  @impl true
  def handle_params(params, _, socket) do
    with {:ok, game} <- Game.find(params["game_id"]) do
      CopiWeb.Endpoint.subscribe(topic(params["game_id"]))

      current_round = if game.finished_at do
        game.rounds_played
      else
        game.rounds_played + 1
      end

      case Want.integer(params["round"], min: 1, max: current_round, default: current_round) do
        {:ok, requested_round} ->
          {:noreply, socket |> assign(:game, game) |> assign(:requested_round, requested_round)}
        {:error, _reason} ->
          {:ok, redirect(socket, to: "/error")}
      end

    else
      {:error, _reason} ->
        {:ok, redirect(socket, to: "/error")}
    end
  end

  @impl true
  def handle_info(%{topic: message_topic, event: "game:updated", payload: updated_game}, socket) do
    cond do
      topic(updated_game.id) == message_topic ->
        {:noreply, assign(socket, :game, updated_game) |> assign(:requested_round, updated_game.rounds_played + 1)}
      true ->
        {:noreply, socket}
    end
  end

  @impl true
  def handle_event("start_game", _, socket) do
    game = socket.assigns.game

    if game.started_at do
      # Do nothing, game's already started
    else
      all_cards = Copi.Cornucopia.list_cards_shuffled()
      players = game.players

      all_cards
      |> Enum.with_index
      |> Enum.each(fn({card, i}) ->
        Copi.Repo.insert! %DealtCard{
          card_id: card.id,
          player_id: Enum.fetch!(players, rem(i, Enum.count(players))).id
        }
      end)

      Copi.Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)} )

      {:ok, updated_game} = Game.find(game.id)
      CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

      {:noreply, assign(socket, :game, updated_game)}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end

  def unplayed_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round == nil end)
  end

  def played_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round != nil end)
  end

  def card_played_in_round(cards, round) do
    dealt_card = Enum.find(cards, fn card -> card.played_in_round == round end)

    if dealt_card, do: dealt_card.card, else: nil
  end
end
