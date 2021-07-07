defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.Cornucopia.Game


  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
    with {:ok, game} <- Game.find(game_id) do

      player = Enum.find(game.players, fn player -> player.id == player_id end)
      dealt_card = Enum.find(player.dealt_cards, fn dealt_card -> Integer.to_string(dealt_card.id) == dealt_card_id end)

      if player && dealt_card do
        dealt_card = Ecto.Changeset.change dealt_card, played_in_round: game.rounds_played + 1

        case Copi.Repo.update dealt_card do
          {:ok, dealt_card} ->
            CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", game)
            conn |> json(%{"id" => dealt_card.id})
          {:error, _changeset} ->
            conn |> json(%{"error" => "Could not update dealt card"})
        end




      else
        conn |> json(%{"error" => "Could not find player and dealt card"})
      end
    else
      {:error, _reason} -> conn |> json(%{"error" => "Could not find game"})
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
