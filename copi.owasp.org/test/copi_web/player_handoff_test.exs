defmodule CopiWeb.PlayerHandoffTest do
  use ExUnit.Case, async: true

  alias CopiWeb.PlayerHandoff

  test "round trips a purpose-bound game and player capability" do
    game_id = "01HV000000000000000000001A"
    player_id = "01HV000000000000000000002B"

    assert {:ok, %{game_id: ^game_id, player_id: ^player_id}} =
             game_id
             |> PlayerHandoff.sign(player_id)
             |> PlayerHandoff.verify()
  end

  test "expires after five minutes" do
    assert PlayerHandoff.max_age_seconds() == 300

    expired_token =
      PlayerHandoff.sign(
        "01HV000000000000000000001A",
        "01HV000000000000000000002B",
        signed_at: System.system_time(:second) - 301
      )

    assert {:error, :invalid} = PlayerHandoff.verify(expired_token)
  end

  test "rejects invalid and non-binary tokens" do
    assert {:error, :invalid} = PlayerHandoff.verify("invalid")
    assert {:error, :invalid} = PlayerHandoff.verify(nil)
  end

  test "does not accept a player creation capability" do
    capability =
      CopiWeb.PlayerCapability.sign(
        "01HV000000000000000000001A",
        "01HV000000000000000000002B"
      )

    assert {:error, :invalid} = PlayerHandoff.verify(capability)
  end
end
