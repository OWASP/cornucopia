defmodule CopiWeb.ResilienceTest do
  use ExUnit.Case, async: false

  alias CopiWeb.Resilience

  test "returns configured resilience values" do
    old = Application.get_env(:copi, :resilience)

    Application.put_env(:copi, :resilience,
      retry_delay_ms: 321,
      max_game_load_retries: 7,
      max_player_load_retries: 5
    )

    assert Resilience.retry_delay_ms() == 321
    assert Resilience.max_game_load_retries() == 7
    assert Resilience.max_player_load_retries() == 5

    if old do
      Application.put_env(:copi, :resilience, old)
    else
      Application.delete_env(:copi, :resilience)
    end
  end

  test "falls back to defaults when config is missing" do
    old = Application.get_env(:copi, :resilience)
    Application.delete_env(:copi, :resilience)

    assert Resilience.retry_delay_ms() == 750
    assert Resilience.max_game_load_retries() == 2
    assert Resilience.max_player_load_retries() == 2

    if old do
      Application.put_env(:copi, :resilience, old)
    end
  end
end
