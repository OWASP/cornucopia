defmodule CopiWeb.PlayerHandoff do
  @moduledoc false

  @salt "player-handoff"
  @max_age_seconds 5 * 60

  def sign(game_id, player_id, opts \\ []) do
    Phoenix.Token.sign(
      CopiWeb.Endpoint,
      @salt,
      %{
        "purpose" => "player_handoff",
        "game_id" => game_id,
        "player_id" => player_id
      },
      opts
    )
  end

  def verify(token) when is_binary(token) do
    case Phoenix.Token.verify(CopiWeb.Endpoint, @salt, token, max_age: @max_age_seconds) do
      {:ok,
       %{
         "purpose" => "player_handoff",
         "game_id" => game_id,
         "player_id" => player_id
       }}
      when is_binary(game_id) and is_binary(player_id) ->
        {:ok, %{game_id: game_id, player_id: player_id}}

      _ ->
        {:error, :invalid}
    end
  end

  def verify(_token), do: {:error, :invalid}

  def max_age_seconds, do: @max_age_seconds
end
