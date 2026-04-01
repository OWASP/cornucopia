defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.Cornucopia.Game
  alias Copi.Repo
  import Ecto.Query

  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
    with {:ok, game} <- Game.find(game_id) do
      player = Enum.find(game.players, fn player -> player.id == player_id end)
      dealt_card = Enum.find(player.dealt_cards, fn dealt_card -> Integer.to_string(dealt_card.id) == dealt_card_id end)

      if player && dealt_card do
        current_round = game.rounds_played + 1

        cond do
          dealt_card.played_in_round ->
            conn |> put_status(:not_acceptable) |> json(%{"error" => "Card already played"})
          Enum.find(player.dealt_cards, fn dealt_card -> dealt_card.played_in_round == current_round end) ->
            conn |> put_status(:forbidden) |> json(%{"error" => "Player already played a card in this round"})
          true ->
            # Atomic update to prevent race conditions
            case play_card_atomically(dealt_card, current_round) do
              {:ok, updated_card} ->
                with {:ok, updated_game} <- Game.find(game.id) do
                  CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", updated_game)
                else
                  {:error, _reason} ->
                    conn |> put_status(:internal_server_error) |> json(%{"error" => "Could not find updated game"})
                end

                conn |> json(%{"id" => updated_card.id})
              {:error, :already_played} ->
                conn |> put_status(:conflict) |> json(%{"error" => "Card was already played by another request"})
              {:error, _changeset} ->
                conn |> put_status(:internal_server_error) |> json(%{"error" => "Could not update dealt card"})
            end
        end
      else
        conn |> put_status(:not_found) |> json(%{"error" => "Player not found in this game"})
      end
    else
      {:error, _reason} -> conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})
    end
  end

  # Atomic card play operation to prevent race conditions
  defp play_card_atomically(dealt_card, current_round) do
    # Use Ecto's atomic operations to prevent race conditions
    from(dc in Copi.Cornucopia.DealtCard, where: dc.id == ^dealt_card.id and is_nil(dc.played_in_round))
    |> Repo.update_all([set: [played_in_round: current_round]], returning: true)
    |> case do
      {1, [updated_card]} -> {:ok, updated_card}
      {0, []} -> {:error, :already_played}
    end
  end
  def topic(game_id) do
    "game:#{game_id}"
  end
end