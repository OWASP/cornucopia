defmodule CopiWeb.PlayerCapabilityTest do
  use ExUnit.Case, async: true

  alias CopiWeb.PlayerCapability

  test "verify/3 returns :ok for a matching token" do
    game_id = "01HV000000000000000000001A"
    player_id = "01HV000000000000000000002B"
    token = PlayerCapability.sign(game_id, player_id)

    assert :ok = PlayerCapability.verify(token, game_id, player_id)
  end

  test "verify/3 returns an error for a different game id" do
    game_id = "01HV000000000000000000001A"
    other_game_id = "01HV000000000000000000003C"
    player_id = "01HV000000000000000000002B"
    token = PlayerCapability.sign(game_id, player_id)

    assert {:error, :invalid} = PlayerCapability.verify(token, other_game_id, player_id)
  end

  test "verify/3 returns an error for a different player id" do
    game_id = "01HV000000000000000000001A"
    player_id = "01HV000000000000000000002B"
    other_player_id = "01HV000000000000000000004D"
    token = PlayerCapability.sign(game_id, player_id)

    assert {:error, :invalid} = PlayerCapability.verify(token, game_id, other_player_id)
  end

  test "verify/3 returns an error for an invalid token" do
    assert {:error, :invalid} = PlayerCapability.verify("bad_token", "game", "player")
  end

  test "verify/1 returns an error for non-binary input" do
    assert {:error, :invalid} = PlayerCapability.verify(nil)
    assert {:error, :invalid} = PlayerCapability.verify(123)
  end
end
