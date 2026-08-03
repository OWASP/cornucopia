defmodule CopiWeb.PlayerSessions do
  @moduledoc false

  @max_entries 20

  def add(session_value, game_id, player_id) do
    entry = %{"game_id" => game_id, "player_id" => player_id}

    session_value
    |> entries()
    |> Enum.reject(&(&1 == entry))
    |> then(&[entry | &1])
    |> Enum.take(@max_entries)
  end

  def authorized?(session_value, game_id, player_id) do
    Enum.any?(entries(session_value), fn entry ->
      entry == %{"game_id" => game_id, "player_id" => player_id}
    end)
  end

  def player_ids_for_game(session_value, game_id) do
    session_value
    |> entries()
    |> Enum.filter(&(&1["game_id"] == game_id))
    |> Enum.map(& &1["player_id"])
  end

  def remove(session_value, game_id, player_id) do
    entry = %{"game_id" => game_id, "player_id" => player_id}
    Enum.reject(entries(session_value), &(&1 == entry))
  end

  def entries(%{"game_id" => game_id, "player_id" => player_id})
      when is_binary(game_id) and is_binary(player_id) do
    [%{"game_id" => game_id, "player_id" => player_id}]
  end

  def entries(entries) when is_list(entries) do
    Enum.filter(entries, fn
      %{"game_id" => game_id, "player_id" => player_id}
      when is_binary(game_id) and is_binary(player_id) ->
        true

      _ ->
        false
    end)
  end

  def entries(_session_value), do: []
end
