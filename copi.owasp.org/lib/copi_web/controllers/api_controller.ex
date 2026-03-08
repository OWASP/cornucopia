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

        # Atomic update to prevent race conditions and enforce one-card-per-round invariant
        case play_card_atomically(dealt_card, player.id, current_round) do
          {:ok, updated_card} ->
            with {:ok, updated_game} <- Game.find(game.id) do
              CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", updated_game)
              conn |> json(%{"id" => updated_card.id})
            else
              {:error, _reason} ->
                conn |> put_status(:internal_server_error) |> json(%{"error" => "Could not find updated game"})
            end
          {:error, :already_played} ->
            conn |> put_status(:conflict) |> json(%{"error" => "Card was already played by another request"})
          {:error, :player_already_played} ->
            conn |> put_status(:forbidden) |> json(%{"error" => "Player already played a card in this round"})
          {:error, _changeset} ->
            conn |> put_status(:internal_server_error) |> json(%{"error" => "Could not update dealt card"})
        end
      else
        conn |> put_status(:not_found) |> json(%{"error" => "Could not find player and dealt card"})
      end
    else
      {:error, _reason} -> conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})
    end
  end

  # Atomic card play operation to prevent race conditions and enforce one-card-per-round invariant
  defp play_card_atomically(dealt_card, player_id, current_round) do
    # Use Ecto's atomic operations to prevent race conditions and enforce invariants
    from(dc in Copi.Cornucopia.DealtCard, 
      where: dc.id == ^dealt_card.id and is_nil(dc.played_in_round))
    |> Repo.update_all([set: [played_in_round: current_round]], returning: true)
    |> case do
      {1, [updated_card]} -> 
        # Check if this player already played a card in this round
        case Repo.get_by(Copi.Cornucopia.DealtCard, 
               [player_id: player_id, played_in_round: current_round], 
               limit: 2) do
          nil -> {:ok, updated_card}
          [%{id: id}] when id == updated_card.id -> {:ok, updated_card}
          _ -> 
            # Player already played a different card this round, rollback
            Repo.delete_all(from(dc in Copi.Cornucopia.DealtCard, 
                              where: dc.id == ^updated_card.id))
            {:error, :player_already_played}
        end
      {0, []} -> {:error, :already_played}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
