defmodule CopiWeb.PlayerLive.Show do
  use CopiWeb, :live_view
  use Phoenix.Component

  alias Copi.Cornucopia.Player
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.DealtCard

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
  def handle_info(%{topic: _message_topic, event: "game:updated", payload: updated_game}, socket) do
    with {:ok, updated_player} <- Player.find(socket.assigns.player.id) do
      {:noreply, socket |> assign(:game, updated_game) |> assign(:player, updated_player)}
    else
      {:error, _reason} ->
        {:ok, redirect(socket, to: "/error")}
    end
  end

  @impl true
  def handle_event("next_round", _, socket) do
    game = socket.assigns.game

    if round_open?(game) do
      # Somehow we've had a request to advance to the next round with players still to play, possibly a race condition, ignore

    else
      Copi.Cornucopia.update_game(game, %{rounds_played: game.rounds_played + 1})

      if last_round?(game) do
        Copi.Cornucopia.update_game(game, %{finished_at: DateTime.truncate(DateTime.utc_now(), :second)} )
      end
    end

    {:ok, updated_game} = Game.find(game.id)

    CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

    {:noreply, assign(socket, :game, updated_game)}
  end

  @impl true
  def handle_event("toggle_vote", %{"dealt_card_id" => dealt_card_id}, socket) do
    game = socket.assigns.game
    player = socket.assigns.player

    {:ok, dealt_card} = DealtCard.find(dealt_card_id)

    vote = get_vote(dealt_card, player)

    if vote do
      IO.puts("player has voted")
      Copi.Repo.delete!(vote)
    else
      IO.puts("player hasn't voted")
      case Copi.Repo.insert(%Copi.Cornucopia.Vote{dealt_card_id: String.to_integer(dealt_card_id), player_id: player.id}) do
        {:ok, _vote} ->
          IO.puts("voted successfully")
        {:error, _changeset} ->
          IO.puts("voting failed")
      end
    end

    {:ok, updated_game} = Game.find(game.id)

    CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

    {:noreply, assign(socket, :game, updated_game)}
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
    Enum.find(cards, fn card -> card.played_in_round == round end)
  end

  def player_first(players, player) do
    Enum.sort_by(players, &(&1.id != player.id))
  end

  def round_open?(game) do
    latest_round = game.rounds_played + 1

    players_still_to_play = game.players |> Enum.filter(fn player -> Enum.find(player.dealt_cards, fn card -> card.played_in_round == latest_round end) == nil end)

    Enum.count(players_still_to_play) > 0
  end

  def round_closed?(game) do
    !round_open?(game)
  end

  def last_round?(game) do
    players_with_no_cards = game.players |> Enum.filter(fn player -> Enum.find(player.dealt_cards, fn card -> card.played_in_round == nil end) == nil end)

    Enum.count(players_with_no_cards) > 0
  end

  def get_vote(dealt_card, player) do
    Enum.find(dealt_card.votes, fn vote -> vote.player_id == player.id end)
  end

  def all_dealt_cards(game) do
    Enum.reduce(game.players, [], fn player, cards -> player.dealt_cards ++ cards end)
  end

  def ordered_cards_played_in_round(game, round) do
    all_dealt_cards(game)
      |> Enum.filter(fn card -> card.played_in_round == round end)
      |> Enum.sort_by(&(&1.updated_at))
  end

  def display_game_session(edition) do
    case edition do
      "ecommerce" -> "Cornucopia Web Session:"
      "masvs" -> "Cornucopia Mobile Session:"
      _ -> "EoP Session:"
    end
  end
end
