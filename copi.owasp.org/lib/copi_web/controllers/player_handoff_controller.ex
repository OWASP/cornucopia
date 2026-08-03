defmodule CopiWeb.PlayerHandoffController do
  use CopiWeb, :controller

  alias Copi.Cornucopia.Player
  alias Copi.PlayerCapabilityRegistry
  alias CopiWeb.PlayerHandoff
  alias CopiWeb.PlayerSessions

  @resume_player_session_key "resume_player_session"

  def redeem(conn, %{"token" => token}) do
    with {:ok, %{game_id: game_id, player_id: player_id}} <- PlayerHandoff.verify(token),
         :ok <- validate_ulid_format(game_id),
         :ok <- validate_ulid_format(player_id),
         {:ok, %{game_id: ^game_id}} <- Player.find(player_id),
         :ok <- PlayerCapabilityRegistry.consume(token) do
      player_sessions =
        conn
        |> get_session(@resume_player_session_key)
        |> PlayerSessions.add(game_id, player_id)

      conn
      |> configure_session(renew: true)
      |> put_session(@resume_player_session_key, player_sessions)
      |> put_resp_header("cache-control", "no-store")
      |> redirect(to: "/games/#{game_id}/players/#{player_id}")
    else
      _ ->
        conn
        |> put_resp_header("cache-control", "no-store")
        |> put_flash(:error, "This handoff link is invalid, expired, or has already been used.")
        |> redirect(to: "/games")
    end
  end

  defp validate_ulid_format(id) when is_binary(id) do
    with 26 <- String.length(id),
         {:ok, _ulid} <- Ecto.ULID.cast(id) do
      :ok
    else
      _ -> :invalid_format
    end
  end
end
