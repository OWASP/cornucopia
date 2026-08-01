defmodule CopiWeb.PlayerSessionsTest do
  use ExUnit.Case, async: true

  alias CopiWeb.PlayerSessions

  test "adds, authorizes, lists, and removes exact game/player pairs" do
    sessions =
      nil
      |> PlayerSessions.add("game-1", "player-1")
      |> PlayerSessions.add("game-1", "player-2")
      |> PlayerSessions.add("game-2", "player-3")

    assert PlayerSessions.authorized?(sessions, "game-1", "player-1")
    assert PlayerSessions.authorized?(sessions, "game-1", "player-2")
    refute PlayerSessions.authorized?(sessions, "game-1", "player-3")
    refute PlayerSessions.authorized?(sessions, "game-2", "player-1")

    assert PlayerSessions.player_ids_for_game(sessions, "game-1") == ["player-2", "player-1"]

    remaining = PlayerSessions.remove(sessions, "game-1", "player-2")
    refute PlayerSessions.authorized?(remaining, "game-1", "player-2")
    assert PlayerSessions.authorized?(remaining, "game-1", "player-1")
  end

  test "moves a duplicate pair to the front without storing it twice" do
    sessions = [
      %{"game_id" => "game-2", "player_id" => "player-2"},
      %{"game_id" => "game-1", "player_id" => "player-1"}
    ]

    assert PlayerSessions.add(sessions, "game-1", "player-1") == [
             %{"game_id" => "game-1", "player_id" => "player-1"},
             %{"game_id" => "game-2", "player_id" => "player-2"}
           ]
  end

  test "accepts the legacy single-entry map and rejects malformed session data" do
    legacy = %{"game_id" => "game-1", "player_id" => "player-1"}

    assert PlayerSessions.entries(legacy) == [legacy]

    malformed = [
      legacy,
      %{"game_id" => "game-2"},
      %{"game_id" => 2, "player_id" => "player-2"},
      :invalid
    ]

    assert PlayerSessions.entries(malformed) == [legacy]
    assert PlayerSessions.entries(nil) == []
    assert PlayerSessions.entries(%{}) == []
  end

  test "limits a browser session to the twenty most recently added pairs" do
    sessions =
      Enum.reduce(1..25, [], fn number, entries ->
        PlayerSessions.add(entries, "game-#{number}", "player-#{number}")
      end)

    assert length(sessions) == 20
    assert hd(sessions) == %{"game_id" => "game-25", "player_id" => "player-25"}
    assert List.last(sessions) == %{"game_id" => "game-6", "player_id" => "player-6"}
    refute PlayerSessions.authorized?(sessions, "game-5", "player-5")
  end
end
