defmodule CopiWeb.PlayerCapability do
  @moduledoc false

  @salt "player-capability"
  @max_age 5 * 60

  def sign(game_id, player_id) do
    Phoenix.Token.sign(CopiWeb.Endpoint, @salt, %{
      "purpose" => "player",
      "game_id" => game_id,
      "player_id" => player_id
    })
  end

  def verify(token) when is_binary(token) do
    case Phoenix.Token.verify(CopiWeb.Endpoint, @salt, token, max_age: @max_age) do
      {:ok, %{"purpose" => "player", "game_id" => game_id, "player_id" => player_id}}
      when is_binary(game_id) and is_binary(player_id) ->
        {:ok, %{game_id: game_id, player_id: player_id}}

      _ ->
        {:error, :invalid}
    end
  end

  def verify(_token), do: {:error, :invalid}

  def verify(token, game_id, player_id) do
    case verify(token) do
      {:ok, %{game_id: ^game_id, player_id: ^player_id}} -> :ok
      _ -> {:error, :invalid}
    end
  end
end
