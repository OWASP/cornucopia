defmodule CopiWeb.GameLive.ShowPureTest do
  use ExUnit.Case, async: true

  alias CopiWeb.GameLive.Show

  test "display_game_session returns expected labels" do
    assert Show.display_game_session("webapp") == "Cornucopia Web Session:"
    assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
    assert Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
    assert Show.display_game_session("unknown") == "EoP Session:"
  end

  test "latest_version returns a version number for any edition" do
    for edition <- ["webapp", "ecommerce", "mobileapp", "mlsec", "cumulus", "masvs", "eop", "dbd", "unknown"] do
      assert {_version, ""} = Float.parse(Show.latest_version(edition))
    end
  end

  test "card_played_in_round finds card or returns nil" do
    cards = [%{played_in_round: 1, id: "a"}, %{played_in_round: 3, id: "b"}]
    assert Show.card_played_in_round(cards, 3) == %{played_in_round: 3, id: "b"}
    assert Show.card_played_in_round(cards, 2) == nil
  end

  test "topic builds topic string" do
    assert Show.topic(42) == "game:42"
    assert Show.topic("abc") == "game:abc"
  end

  test "put_uri_hook assigns uri and continues" do
    socket = %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}}}

    assert {:cont, socket} = Show.put_uri_hook(%{}, "http://localhost/games/1", socket)
    assert socket.assigns.uri == "http://localhost/games/1"
  end

  test "on_mount default raises when not mounted via router live/3" do
    socket = %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}}}

    assert_raise RuntimeError, ~r/view was not mounted at the router with the live\/3 macro/, fn ->
      Show.on_mount(:default, %{}, %{}, socket)
    end
  end
end
