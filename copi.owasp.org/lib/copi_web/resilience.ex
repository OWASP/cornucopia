defmodule CopiWeb.Resilience do
  @moduledoc false

  @defaults [
    retry_delay_ms: 750,
    max_game_load_retries: 2,
    max_player_load_retries: 2
  ]

  def retry_delay_ms do
    config(:retry_delay_ms)
  end

  def max_game_load_retries do
    config(:max_game_load_retries)
  end

  def max_player_load_retries do
    config(:max_player_load_retries)
  end

  defp config(key) do
    :copi
    |> Application.get_env(:resilience, @defaults)
    |> Keyword.get(key, Keyword.fetch!(@defaults, key))
  end
end