defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.PlayerCapabilityRegistry
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.Player
  alias CopiWeb.PlayerCapability
  alias CopiWeb.PlayerSessions

  require Logger
  import Ecto.Query, only: [from: 2, subquery: 1]

  @resume_player_session_key "resume_player_session"

  def exchange_player_capability(conn, %{"capability" => capability}) do
    with {:ok, %{game_id: game_id, player_id: player_id}} <- PlayerCapability.verify(capability),
         :ok <- validate_ulid_format(game_id),
         :ok <- validate_ulid_format(player_id),
         {:ok, %{game_id: ^game_id}} <- Player.find(player_id),
         :ok <- PlayerCapabilityRegistry.consume(capability) do
      player_sessions =
        conn
        |> get_session(@resume_player_session_key)
        |> PlayerSessions.add(game_id, player_id)

      conn
      |> configure_session(renew: true)
      |> put_session(@resume_player_session_key, player_sessions)
      |> put_resp_header("cache-control", "no-store")
      |> json(%{"redirect_to" => "/games/#{game_id}/players/#{player_id}"})
    else
      _ ->
        conn
        |> put_status(:unauthorized)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Invalid or expired player capability"})
    end
  end

  def exchange_player_capability(conn, _params) do
    conn
    |> put_status(:bad_request)
    |> put_resp_header("cache-control", "no-store")
    |> json(%{"error" => "Invalid player capability request"})
  end

  def clear_player_session(conn, %{"game_id" => game_id, "player_id" => player_id}) do
    with :ok <- validate_ulid_format(game_id),
         :ok <- validate_ulid_format(player_id) do
        remaining_sessions =
          conn
          |> get_session(@resume_player_session_key)
          |> PlayerSessions.remove(game_id, player_id)

        conn =
          if remaining_sessions == [] do
            delete_session(conn, @resume_player_session_key)
          else
            put_session(conn, @resume_player_session_key, remaining_sessions)
          end

        conn
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"ok" => true})
    else
      :invalid_format ->
        conn
        |> put_status(:bad_request)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Invalid player session parameters"})
    end
  end

  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
    if PlayerSessions.authorized?(get_session(conn, @resume_player_session_key), game_id, player_id) do
      play_card_as(conn, game_id, player_id, dealt_card_id)
    else
      conn
      |> put_status(:unauthorized)
      |> json(%{"error" => "Valid player session required"})
    end
  end

  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id}) do
    Logger.warning(
      "Missing dealt_card_id for play_card request: game_id=#{inspect(game_id)}, player_id=#{inspect(player_id)}"
    )

    conn
    |> put_status(:bad_request)
    |> json(%{"error" => "Missing required parameter: dealt_card_id"})
  end

  def play_card(conn, params) do
    Logger.warning("Invalid play_card request params: #{inspect(params)}")

    conn
    |> put_status(:bad_request)
    |> json(%{"error" => "Invalid request parameters"})
  end

  defp play_card_as(conn, game_id, player_id, dealt_card_id) do
    game_mod = Application.get_env(:copi, :api_game_module, Game) || Game
    repo_mod = Application.get_env(:copi, :api_repo_module, Copi.Repo) || Copi.Repo

    case game_mod.find(game_id) do
      {:ok, game} ->
        player = Enum.find(game.players, fn player -> player.id == player_id end)

        if player do
          dealt_card = Enum.find(player.dealt_cards, fn dealt_card -> Integer.to_string(dealt_card.id) == dealt_card_id end)

          if dealt_card do
            current_round = game.rounds_played + 1

            cond do
              dealt_card.played_in_round ->
                conn |> put_status(:not_acceptable) |> json(%{"error" => "Card already played"})

              Enum.find(player.dealt_cards, fn dealt_card -> dealt_card.played_in_round == current_round end) ->
                conn |> put_status(:forbidden) |> json(%{"error" => "Player already played a card in this round"})

              true ->
                result =
                  Copi.Repo.transaction(fn ->
                    # Lock the player row to serialize plays by the same player so
                    # the conditional update below always sees the freshest state.
                    case Copi.Repo.get(Copi.Cornucopia.Player, player_id, lock: "FOR UPDATE") do
                      nil ->
                        Copi.Repo.rollback(:player_missing)

                      _player ->
                        case repo_mod.update_all(
                               from(dc in Copi.Cornucopia.DealtCard,
                                 where: dc.id == ^dealt_card.id and is_nil(dc.played_in_round),
                                 where:
                                   not exists(
                                     subquery(
                                       from(pc in Copi.Cornucopia.DealtCard,
                                         where:
                                           pc.player_id == ^player_id and
                                             pc.played_in_round == ^current_round and
                                             pc.id != ^dealt_card.id,
                                         select: pc.id
                                       )
                                     )
                                   )
                               ),
                               set: [played_in_round: current_round]
                             ) do
                          {1, _} ->
                            :ok

                          {0, _} ->
                            Copi.Repo.rollback(:already_played)

                          {:error, reason} ->
                            Copi.Repo.rollback(reason)
                        end
                    end
                  end)

                case result do
                  {:ok, :ok} ->
                    case game_mod.find(game.id) do
                      {:ok, updated_game} ->
                        CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", updated_game)
                        conn |> json(%{"id" => dealt_card.id})

                      {:error, :not_found} ->
                        Logger.warning("Game disappeared after card update: #{inspect(game.id)}")
                        conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})

                      {:error, reason} ->
                        Logger.warning("Transient game reload failure after card update for game_id=#{inspect(game.id)}, reason=#{inspect(reason)}")
                        conn |> put_status(:service_unavailable) |> json(%{"error" => "Temporary service issue. Please retry."})
                    end

                  {:error, :already_played} ->
                    Logger.warning(
                      "Card play race for dealt_card_id=#{inspect(dealt_card.id)}, player_id=#{inspect(player_id)} in game_id=#{inspect(game_id)}"
                    )

                    conn
                    |> put_status(:conflict)
                    |> json(%{"error" => "Card was already played by another request"})

                  {:error, :player_missing} ->
                    Logger.warning(
                      "Player #{inspect(player_id)} disappeared before card play in game_id=#{inspect(game_id)}"
                    )

                    conn
                    |> put_status(:conflict)
                    |> json(%{"error" => "Card was already played by another request"})

                  {:error, reason} ->
                    Logger.warning(
                      "Card play transaction failed for game_id=#{inspect(game_id)}, player_id=#{inspect(player_id)}, reason=#{inspect(reason)}"
                    )

                    conn
                    |> put_status(:service_unavailable)
                    |> json(%{"error" => "Temporary service issue. Please retry."})
                end
            end
          else
            Logger.debug("Dealt card #{inspect(dealt_card_id)} not found for player: #{inspect(player_id)}")
            conn |> put_status(:not_found) |> json(%{"error" => "Could not find player and dealt card"})
          end
        else
          Logger.debug("Player #{inspect(player_id)} not found in game: #{inspect(game_id)}")
          conn |> put_status(:not_found) |> json(%{"error" => "Player not found in this game"})
        end

      {:error, :not_found} ->
        Logger.debug("Game not found: #{inspect(game_id)}")
        conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})

      {:error, reason} ->
        Logger.debug("Transient game lookup failure for game_id=#{inspect(game_id)}, reason=#{inspect(reason)}")
        conn |> put_status(:service_unavailable) |> json(%{"error" => "Temporary service issue. Please retry."})
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end

  defp validate_ulid_format(id) when is_binary(id) do
    case String.length(id) do
      26 ->
        case Ecto.ULID.cast(id) do
          {:ok, _} -> :ok
          :error -> :invalid_format
        end

      _ ->
        :invalid_format
    end
  end

  defp validate_ulid_format(_), do: :invalid_format
end