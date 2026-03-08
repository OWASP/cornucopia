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
    # Use database transaction to ensure atomicity and prevent race conditions
    Repo.transaction(fn ->
      # First, try to lock player's cards for this round by checking existing plays
      existing_cards = Repo.all(
        from(dc in Copi.Cornucopia.DealtCard, 
          where: dc.player_id == ^player_id and dc.played_in_round == ^current_round)
      )
      
      if length(existing_cards) > 0 do
        {:error, :player_already_played}
      else
        # Now atomically update the card with played_in_round
        from(dc in Copi.Cornucopia.DealtCard, 
          where: dc.id == ^dealt_card.id and is_nil(dc.played_in_round))
        |> Repo.update_all([set: [played_in_round: current_round]], returning: true)
        |> case do
          {1, [updated_card]} -> {:ok, updated_card}
          {0, []} -> {:error, :already_played}
        end
      end
    end)
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
