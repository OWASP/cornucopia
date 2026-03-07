defmodule CopiWeb.GameLive.ShowPureTest do
  use ExUnit.Case, async: true

  alias CopiWeb.GameLive.Show

  test "display_game_session returns expected labels" do
    assert Show.display_game_session("webapp") == "Cornucopia Web Session:"
    assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
    assert Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
    assert Show.display_game_session("unknown") == "EoP Session:"
  end

  test "latest_version returns expected versions" do
    assert Show.latest_version("webapp") == "2.2"
    assert Show.latest_version("ecommerce") == "1.22"
    assert Show.latest_version("eop") == "5.1"
    assert Show.latest_version("other") == "1.0"
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
end
