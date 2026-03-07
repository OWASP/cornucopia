defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    {:ok, assign(socket, :client_ip, ip)}
  end

  def on_mount(:default, _params, _session, socket) do
    socket = attach_hook(socket, :current_path_hook, :handle_params, &put_uri_hook/3)
    {:cont, socket}
  end

  def put_uri_hook(_params, uri, socket), do: {:cont, assign(socket, uri: uri)}

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
          {:noreply, redirect(socket, to: "/error")}
      end

    else
      {:error, _reason} ->
        {:noreply, redirect(socket, to: "/error")}
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

    cond do
      game.started_at ->
        # Game already started – idempotent noop; always return a valid LiveView reply.
        # ASVS V2.3.3 – never allow skipping steps or re-triggering a completed flow.
        {:noreply, socket}

      length(game.players) < 3 ->
        # Minimum 3 players required (aligned with UI requirement)
        {:noreply,
         socket
         |> put_flash(:error, "Cannot start game: At least 3 players are required to start.")
         |> assign(:game, game)}

      true ->
        # Valid player count (3+), proceed with game start
        all_cards = Copi.Cornucopia.list_cards_shuffled(game.edition, game.suits, latest_version(game.edition))
        players = game.players

        # ASVS V2.3.3 – wrap dealing + game start in one atomic transaction so either
        # all cards are dealt and the game is marked started, or nothing is persisted.
        case Copi.Cornucopia.deal_cards_for_game(game, players, all_cards) do
          {:ok, _result} ->
            {:ok, updated_game} = Game.find(game.id)
            CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)
            {:noreply, assign(socket, :game, updated_game)}

          {:error, _step, _reason} ->
            # ASVS V16.5 – fail gracefully with a generic message; never crash the
            # LiveView process or expose internal error details to the client.
            {:noreply, put_flash(socket, :error, "Failed to deal cards. Please try again.")}
        end
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end

  @spec card_played_in_round(any, any) :: any
  def card_played_in_round(cards, round) do
    Enum.find(cards, fn card -> card.played_in_round == round end)
  end

  def display_game_session(edition) do
    case edition do
      "webapp" -> "Cornucopia Web Session:"
      "ecommerce" -> "Cornucopia Web Session:"
      "mobileapp" -> "Cornucopia Mobile Session:"
      "mlsec" -> "Elevation of MLSec Session:"
      "cumulus" -> "OWASP Cumulus Session:"
      "masvs" -> "Cornucopia Mobile Session:"
      _ -> "EoP Session:"
    end
  end

  def latest_version(edition) do
    case edition do
      "webapp" -> "2.2"
      "ecommerce" -> "1.22"
      "mobileapp" -> "1.1"
      "mlsec" -> "1.0"
      "cumulus" -> "1.1"
      "masvs" -> "1.1"
      "eop" -> "5.1"
      _ -> "1.0"
    end
  end
end
