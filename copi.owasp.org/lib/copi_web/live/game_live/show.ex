defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.DealtCard

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
end
