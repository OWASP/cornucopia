defmodule CopiWeb.PlayerLive.Show do
  use CopiWeb, :live_view
  use Phoenix.Component

  require Logger
  import Ecto.Query

  alias Copi.Cornucopia.Player
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.Vote
  alias Copi.Cornucopia.ContinueVote

  @impl true
  def mount(_params, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    {:ok, assign(socket, :client_ip, ip)}
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
  def handle_info(:proceed_to_next_round, socket) do
    game = socket.assigns.game

    # Clear all continue votes for this game before proceeding to next round
    Copi.Repo.delete_all(from cv in Copi.Cornucopia.ContinueVote, where: cv.game_id == ^game.id)

    # Now proceed to next round
    Copi.Cornucopia.update_game(game, %{rounds_played: game.rounds_played + 1, round_open: true})

    if last_round?(game) do
      Copi.Cornucopia.update_game(game, %{finished_at: DateTime.truncate(DateTime.utc_now(), :second)} )
    end

    {:ok, updated_game} = Game.find(game.id)

    CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

    {:noreply, assign(socket, :game, updated_game)}
  end

  @impl true
  def handle_event("next_round", _, socket) do
    game = socket.assigns.game

    if round_open?(game) do
      # Check if we can continue due to majority continue votes
      if Copi.Cornucopia.Game.can_continue_round?(game) do
        # Close the round and proceed
        Copi.Cornucopia.update_game(game, %{round_open: false})

        # Wait a moment then proceed to next round
        Process.send_after(self(), :proceed_to_next_round, 100)

        {:noreply, assign(socket, :game, game)}
      else
        # Somehow we've had a request to advance to the next round with players still to play, possibly a race condition, ignore
        {:noreply, socket}
      end
    else
      Copi.Cornucopia.update_game(game, %{rounds_played: game.rounds_played + 1, round_open: true})

      if last_round?(game) do
        Copi.Cornucopia.update_game(game, %{finished_at: DateTime.truncate(DateTime.utc_now(), :second)} )
      end
    end

    {:ok, updated_game} = Game.find(game.id)

    CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

    {:noreply, assign(socket, :game, updated_game)}
  end

  @impl true
  def handle_event("toggle_continue_vote", _, socket) do
    game = socket.assigns.game
    player = socket.assigns.player

    # Use atomic delete to avoid TOCTOU race condition
    # Try to delete first - if none exists, this is a no-op
    case Copi.Repo.delete_all(
      from cv in ContinueVote,
      where: cv.player_id == ^player.id and cv.game_id == ^game.id
    ) do
      {1, _} ->
        Logger.debug("Continue vote removed for player #{player.id}")
      
      {0, _} ->
        # No vote existed, so insert one
        case Copi.Repo.insert(
          %ContinueVote{player_id: player.id, game_id: game.id},
          on_conflict: :nothing,
          conflict_target: [:player_id, :game_id]
        ) do
          {:ok, _vote} ->
            Logger.debug("Continue vote added for player #{player.id}")
          {:error, changeset} ->
            Logger.warning("Continue voting failed: #{inspect(changeset.errors)}")
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

    # Safely parse dealt_card_id to prevent crashes from invalid input
    case Integer.parse(dealt_card_id) do
      {dealt_card_id_int, _} ->
        # Use atomic delete to avoid TOCTOU race condition
        # Try to delete first - if none exists, this is a no-op
        case Copi.Repo.delete_all(
          from v in Vote,
          where: v.player_id == ^player.id and v.dealt_card_id == ^dealt_card_id_int
        ) do
          {1, _} ->
            Logger.debug("Vote removed for player #{player.id} on card #{dealt_card_id_int}")
          
          {0, _} ->
            # No vote existed, so insert one
            case Copi.Repo.insert(
              %Vote{dealt_card_id: dealt_card_id_int, player_id: player.id},
              on_conflict: :nothing,
              conflict_target: [:player_id, :dealt_card_id]
            ) do
              {:ok, _vote} ->
                Logger.debug("Vote added for player #{player.id} on card #{dealt_card_id_int}")
              {:error, changeset} ->
                Logger.warning("Voting failed: #{inspect(changeset.errors)}")
            end
        end
        {:ok, updated_game} = Game.find(game.id)
        CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)
        {:noreply, assign(socket, :game, updated_game)}
      
      :error ->
        Logger.warning("Invalid dealt_card_id: #{inspect(dealt_card_id)}")
        {:noreply, socket}
    end
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

  def display_game_session(edition) do
    case edition do
      "webapp" -> "Cornucopia Web Session:"
      "ecommerce" -> "Cornucopia Web Session:"
      "mobileapp" -> "Cornucopia Mobile Session:"
      "masvs" -> "Cornucopia Mobile Session:"
      "cumulus" -> "OWASP Cumulus Session:"
      "mlsec" -> "Elevation of MLSec Session:"
      _ -> "EoP Session:"
    end
  end

end
