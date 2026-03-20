defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  require Logger
  
  alias Copi.Cornucopia.Game

  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
    case Game.find(game_id) do
      {:ok, game} ->
        player = Enum.find(game.players, fn player -> player.id == player_id end)
        
        # CRITICAL SECURITY VALIDATION: Ensure player belongs to the specified game
        cond do
          !player ->
            Logger.warning("Security: API play_card attempted - player #{player_id} not found in game #{game_id}, IP: #{get_client_ip(conn)}")
            conn |> put_status(:not_found) |> json(%{"error" => "Could not find player"})
          
          player.game_id != game_id ->
            Logger.warning("Security: API play_card attempted - player #{player_id} does not belong to game #{game_id}, IP: #{get_client_ip(conn)}")
            conn |> put_status(:forbidden) |> json(%{"error" => "Player does not belong to this game"})
          
          true ->
            dealt_card = Enum.find(player.dealt_cards, fn dealt_card -> Integer.to_string(dealt_card.id) == dealt_card_id end)

            cond do
              !dealt_card ->
                Logger.warning("Security: API play_card attempted - dealt_card #{dealt_card_id} not found for player #{player_id}, IP: #{get_client_ip(conn)}")
                conn |> put_status(:not_found) |> json(%{"error" => "Could not find dealt card"})
              
              dealt_card.played_in_round ->
                conn |> put_status(:not_acceptable) |> json(%{"error" => "Card already played"})
              
              Enum.find(player.dealt_cards, fn dealt_card -> dealt_card.played_in_round == game.rounds_played + 1 end) ->
                conn |> put_status(:forbidden) |> json(%{"error" => "Player already played a card in this round"})
              
              true ->
                dealt_card = Ecto.Changeset.change dealt_card, played_in_round: game.rounds_played + 1

                case Copi.Repo.update dealt_card do
                  {:ok, dealt_card} ->
                    with {:ok, updated_game} <- Game.find(game.id) do
                      CopiWeb.Endpoint.broadcast(topic(game.id), "game:updated", updated_game)
                    else
                      {:error, _reason} ->
                        conn |> put_status(:internal_server_error) |> json(%{"error" => "Could not find updated game"})
                    end

                    conn |> json(%{"id" => dealt_card.id})
                  {:error, _changeset} ->
                    conn |> put_status(:internal_server_error) |> json(%{"error" => "Could not update dealt card"})
                end
            end
        end
      
      {:error, _reason} ->
        Logger.warning("Security: API play_card attempted - game #{game_id} not found, IP: #{get_client_ip(conn)}")
        conn |> put_status(:not_found) |> json(%{"error" => "Could not find game"})
    end
  end

  defp get_client_ip(conn) do
    # Get IP from various headers, fallback to remote_ip
    case get_req_header(conn, "x-forwarded-for") do
      [ip | _] -> ip
      [] -> 
        case get_req_header(conn, "x-real-ip") do
          [ip | _] -> ip
          [] -> to_string(:inet_parse.ntoa(conn.remote_ip))
        end
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
