defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.DealtCard

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
        # Game already started, do nothing
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
        player_count = length(players)

        # Deal cards to players in round-robin fashion
        all_cards
        |> Enum.with_index()
        |> Enum.each(fn {card, i} ->
          Copi.Repo.insert!(%DealtCard{
            card_id: card.id,
            player_id: Enum.at(players, rem(i, player_count)).id
          })
        end)

        # Update game with start time and handle potential errors
        case Copi.Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)}) do
          {:ok, updated_game} ->
            CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)
            {:noreply, assign(socket, :game, updated_game)}

          {:error, _changeset} ->
            # If update fails, reload game and show error
            {:ok, reloaded_game} = Game.find(game.id)
            {:noreply,
             socket
             |> put_flash(:error, "Failed to start game. Please try again.")
             |> assign(:game, reloaded_game)}
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
