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

      current_round =
        if game.finished_at do
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
        {:noreply,
         assign(socket, :game, updated_game)
         |> assign(:requested_round, updated_game.rounds_played + 1)}

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
      all_cards = Copi.Cornucopia.list_cards_shuffled(game.edition)
      players = game.players

      all_cards
      |> Enum.with_index()
      |> Enum.each(fn {card, i} ->
        Copi.Repo.insert!(%DealtCard{
          card_id: card.id,
          player_id: Enum.fetch!(players, rem(i, Enum.count(players))).id
        })
      end)

      Copi.Cornucopia.update_game(game, %{
        started_at: DateTime.truncate(DateTime.utc_now(), :second)
      })

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

  def scoring_cards(cards, number_of_players) do
    Enum.filter(cards, fn card ->
      card.played_in_round != nil && Enum.count(card.votes) > (number_of_players - 1) / 2
    end)
  end

  def lead_suit_cards(cards) do
    # Convert to map where {round, [played_cards]}
    Enum.group_by(cards, fn card -> card.played_in_round end)
    # Sort played cards in rounds by when played
    |> Map.new(fn {round, played_cards} ->
      {round, Enum.sort_by(played_cards, & &1.updated_at)}
    end)
    # Back to a list of just the lead suit cards in each round
    |> Enum.flat_map(fn {_round, ordered_played_cards} ->
      Enum.filter(ordered_played_cards, fn card ->
        card.card.category == List.first(ordered_played_cards).card.category or
          card.card.value in ["JokerA", "JokerB"]
      end)
    end)
  end

  def highest_scoring_cards(player, game) do
    # Combine all played cards from all players
    Enum.reduce(game.players, [], fn player, cards ->
      (player.dealt_cards |> played_cards) ++ cards
    end)
    # Filter to just the lead suit cards
    |> lead_suit_cards
    # Filter to just the cards that scored
    |> scoring_cards(Enum.count(game.players))
    # Convert to map where {round, [scoring_cards]}
    |> Enum.group_by(fn card -> card.played_in_round end)
    # Back to a list of just the highest scoring card in each round
    |> Enum.flat_map(fn {_, cards} -> highest_scoring_cards(cards) end)
    # Filter out just the highest scoring cards for the player provided
    |> Enum.filter(fn dealt_card -> dealt_card.player_id == player.id end)
  end

  def highest_scoring_cards(cards) do
    card_order = [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10",
      "J",
      "Q",
      "K",
      "A",
      "JokerB",
      "JokerA"
    ]

    Enum.group_by(cards, fn dealt_card ->
      Enum.find_index(card_order, fn value -> value == dealt_card.card.value end)
    end)
    |> Enum.max_by(fn {index, _cards} -> index end)
    |> elem(1)
  end

  @spec card_played_in_round(any, any) :: any
  def card_played_in_round(cards, round) do
    Enum.find(cards, fn card -> card.played_in_round == round end)
  end
end
