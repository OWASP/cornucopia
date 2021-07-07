defmodule CopiWeb.ApiController do
  use CopiWeb, :controller
  alias Copi.Cornucopia.DealtCard


  def play_card(conn, %{"game_id" => game_id, "player_id" => player_id, "dealt_card_id" => dealt_card_id}) do
    conn |> json(%{"id" => dealt_card_id})
  end
end
