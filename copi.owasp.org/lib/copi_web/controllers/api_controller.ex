defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.Player

  require Logger

  @resume_player_session_key "resume_player_session"

  def persist_player_session(conn, %{"game_id" => game_id, "player_id" => player_id}) do
    with :ok <- validate_ulid_format(game_id),
         :ok <- validate_ulid_format(player_id),
         {:ok, player} <- Player.find(player_id),
         true <- player.game_id == game_id do
      conn
      |> put_session(@resume_player_session_key, %{"game_id" => game_id, "player_id" => player_id})
      |> put_resp_header("cache-control", "no-store")
      |> json(%{"ok" => true})
    else
      :invalid_format ->
        conn
        |> delete_session(@resume_player_session_key)
        |> put_status(:bad_request)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Invalid player session parameters"})

      {:error, :not_found} ->
        conn
        |> delete_session(@resume_player_session_key)
        |> put_status(:not_found)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Player not found"})

      {:error, reason} ->
        Logger.debug("Transient player lookup failure while persisting player session for player_id=#{inspect(player_id)}, reason=#{inspect(reason)}")

        conn
        |> put_status(:service_unavailable)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Temporary service issue. Please retry."})

      false ->
        conn
        |> delete_session(@resume_player_session_key)
        |> put_status(:forbidden)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Player does not belong to this game"})
    end
  end

  def persist_player_session(conn, _params) do
    conn
    |> put_status(:bad_request)
    |> put_resp_header("cache-control", "no-store")
    |> json(%{"error" => "Invalid player session parameters"})
  end

  def clear_player_session(conn, %{"game_id" => game_id}) do
    case validate_ulid_format(game_id) do
      :ok ->
        conn =
          case get_session(conn, @resume_player_session_key) do
            %{"game_id" => ^game_id} -> delete_session(conn, @resume_player_session_key)
            _ -> conn
          end

        conn
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"ok" => true})

      :invalid_format ->
        conn
        |> put_status(:bad_request)
        |> put_resp_header("cache-control", "no-store")
        |> json(%{"error" => "Invalid game identifier"})
    end
  end

  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
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
                dealt_card_changeset = Ecto.Changeset.change(dealt_card, played_in_round: current_round)

                case repo_mod.update(dealt_card_changeset) do
                  {:ok, updated_dealt_card} ->
                    case game_mod.find(game.id) do
                      {:ok, updated_game} ->
                        CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", updated_game)
                        conn |> json(%{"id" => updated_dealt_card.id})

                      {:error, :not_found} ->
                        Logger.warning("Game disappeared after card update: #{inspect(game.id)}")
                        conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})

                      {:error, reason} ->
                        Logger.warning("Transient game reload failure after card update for game_id=#{inspect(game.id)}, reason=#{inspect(reason)}")
                        conn |> put_status(:service_unavailable) |> json(%{"error" => "Temporary service issue. Please retry."})
                    end

                  {:error, changeset} ->
                    Logger.warning("Card update failed for dealt_card_id=#{inspect(dealt_card.id)}, player_id=#{inspect(player_id)}, game_id=#{inspect(game_id)}, errors=#{inspect(changeset.errors)}")
                    conn |> put_status(:unprocessable_entity) |> json(%{"error" => "Could not play card"})
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