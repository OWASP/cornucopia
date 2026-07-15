defmodule CopiWeb.GameLive.Show do
  use CopiWeb, :live_view

  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.DealtCard
  alias CopiWeb.Resilience

  require Logger

  @impl true
  def mount(params, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    resume_player_id = resume_player_id_for_game(session, params["game_id"])
    {:ok, socket |> assign(:client_ip, ip) |> assign(:resume_player_id, resume_player_id)}
  end

  def on_mount(:default, _params, _session, socket) do
    socket = attach_hook(socket, :current_path_hook, :handle_params, &put_uri_hook/3)
    {:cont, socket}
  end

  def put_uri_hook(_params, uri, socket), do: {:cont, assign(socket, uri: uri)}

  @impl true
  def handle_params(params, _, socket) do
    case game_module().find(params["game_id"]) do
      {:ok, game} ->
        CopiWeb.Endpoint.subscribe(topic(params["game_id"]))
        assign_game_and_round(socket, params, game)

      {:error, :not_found} ->
        {:noreply,
         socket
         |> put_flash(:error, "Game not found.")
         |> redirect(to: "/games")}

      {:error, reason} ->
        retry_count = socket.assigns[:game_load_retry_count] || 0

        Logger.debug(
          "Transient game load failure for game_id=#{inspect(params["game_id"])}, retry=#{retry_count}, reason=#{inspect(reason)}"
        )

        cond do
          socket.assigns[:game] && retry_count < Resilience.max_game_load_retries() ->
            Process.send_after(self(), {:retry_game_load, params}, Resilience.retry_delay_ms())

            {:noreply,
             socket
             |> assign(:game_load_retry_count, retry_count + 1)
             |> put_flash(:error, "Temporary issue loading game. Retrying...")}

          socket.assigns[:game] ->
            {:noreply,
             socket
             |> assign(:game_load_retry_count, 0)
             |> put_flash(:error, "Temporary issue loading game. Please try again.")}

          true ->
            {:noreply,
             socket
             |> put_flash(:error, "Temporary issue loading game. Please try again.")
             |> redirect(to: "/games")}
        end
    end
  end

  @impl true
  def handle_info({:retry_game_load, params}, socket) do
    handle_params(params, nil, socket)
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

  defp assign_game_and_round(socket, params, game) do
    current_round = if game.finished_at do
      game.rounds_played
    else
      game.rounds_played + 1
    end

    round_result = if params["round"] do
      Want.integer(params["round"], min: 1, max: current_round)
    else
      {:ok, current_round}
    end

    case round_result do
      {:ok, requested_round} ->
        {:noreply,
         socket
         |> assign(:game, game)
         |> assign(:requested_round, requested_round)
         |> assign(:game_load_retry_count, 0)}

      {:error, _reason} ->
        {:noreply,
         socket
         |> assign(:game, game)
         |> assign(:requested_round, current_round)
         |> assign(:game_load_retry_count, 0)
         |> put_flash(:error, "Invalid round value. Showing current round instead.")}
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
        case start_game_transaction(game) do
          {:ok, updated_game} ->
            CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)
            {:noreply, assign(socket, :game, updated_game)}

          {:error, :not_enough_players} ->
            {:noreply,
             socket
             |> put_flash(:error, "Cannot start game: At least 3 players are required to start.")
             |> assign(:game, game)}

          {:error, :already_started} ->
            {:noreply, socket}

          {:error, reason} ->
            Logger.error("Unable to start game #{game.id}: #{inspect(reason)}")

            {:noreply,
             socket
             |> put_flash(:error, "Unable to start game. Please try again.")
             |> assign(:game, game)}
        end
    end
  end

  defp start_game_transaction(game) do
    Copi.Repo.transaction(fn ->
      locked_game =
        Copi.Repo.get!(Game, game.id, lock: "FOR UPDATE")
        |> Copi.Repo.preload(:players)

      cond do
        locked_game.started_at ->
          Copi.Repo.rollback(:already_started)

        length(locked_game.players) < 3 ->
          Copi.Repo.rollback(:not_enough_players)

        true ->
          all_cards =
            Copi.Cornucopia.list_cards_shuffled(
              locked_game.edition,
              locked_game.suits,
              latest_version(locked_game.edition)
            )

          player_count = length(locked_game.players)

          all_cards
          |> Enum.with_index()
          |> Enum.each(fn {card, i} ->
            case Copi.Repo.insert(%DealtCard{
                   card_id: card.id,
                   player_id: Enum.at(locked_game.players, rem(i, player_count)).id
                 }) do
              {:ok, _dealt_card} -> :ok
              {:error, changeset} -> Copi.Repo.rollback({:card_dealing_failed, changeset})
            end
          end)

          case Copi.Cornucopia.update_game(locked_game, %{
                 started_at: DateTime.truncate(DateTime.utc_now(), :second)
               }) do
            {:ok, updated_game} -> updated_game
            {:error, changeset} -> Copi.Repo.rollback({:game_update_failed, changeset})
          end
      end
    end)
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
      "dbd" -> "Digital Benefits Deck Session:"
      _ -> "EoP Session:"
    end
  end

  def latest_version(edition) do
    case edition do
      "webapp" -> "3.0"
      "ecommerce" -> "1.22"
      "mobileapp" -> "1.1"
      "mlsec" -> "1.0"
      "cumulus" -> "1.1"
      "masvs" -> "1.1"
      "eop" -> "5.1"
      "dbd" -> "1.0"
      _ -> "1.0"
    end
  end

  defp game_module do
    Application.get_env(:copi, :game_live_show_game_module, Game) || Game
  end

  defp resume_player_id_for_game(session, game_id) do
    case session["resume_player_session"] do
      %{"game_id" => ^game_id, "player_id" => player_id} when is_binary(player_id) ->
        case Ecto.ULID.cast(player_id) do
          {:ok, valid_player_id} -> valid_player_id
          :error -> nil
        end

      _ ->
        nil
    end
  end
end
