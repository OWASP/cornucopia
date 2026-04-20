defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.Cornucopia.Game

  # coveralls-ignore-start
  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
    with {:ok, game} <- Game.find(game_id) do
      cond do
        is_nil(game.started_at) ->
          conn |> put_status(:unprocessable_entity) |> json(%{"error" => "Game has not started yet"})

        not is_nil(game.finished_at) ->
          conn |> put_status(:unprocessable_entity) |> json(%{"error" => "Game has already ended"})

        true ->
          player = Enum.find(game.players, fn player -> player.id == player_id end)

          if player do
            dealt_card =
              Enum.find(player.dealt_cards, fn dealt_card ->
                Integer.to_string(dealt_card.id) == dealt_card_id
              end)

            if dealt_card do
              current_round = game.rounds_played + 1

              cond do
                dealt_card.played_in_round ->
                  conn |> put_status(:not_acceptable) |> json(%{"error" => "Card already played"})

                Enum.find(player.dealt_cards, fn dealt_card -> dealt_card.played_in_round == current_round end) ->
                  conn |> put_status(:forbidden) |> json(%{"error" => "Player already played a card in this round"})

                true ->
                  dealt_card = Ecto.Changeset.change(dealt_card, played_in_round: current_round)
                  dealt_card = Copi.Repo.update!(dealt_card)

                  {:ok, updated_game} = Game.find(game.id)
                  CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", updated_game)

                  conn |> json(%{"id" => dealt_card.id})
              end
            else
              conn |> put_status(:not_found) |> json(%{"error" => "Could not find player and dealt card"})
            end
          else
            conn |> put_status(:not_found) |> json(%{"error" => "Player not found in this game"})
          end
      end
    else
      {:error, _reason} -> conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})
    end
  end
  # coveralls-ignore-stop

  def topic(game_id) do
    "game:#{game_id}"
  end
end