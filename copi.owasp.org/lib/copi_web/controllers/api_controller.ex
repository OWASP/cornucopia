defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.Cornucopia.Game

  require Logger

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

  def topic(game_id) do
    "game:#{game_id}"
  end
end