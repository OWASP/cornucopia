defmodule CopiWeb.GameLive.ShowTest do
  use ExUnit.Case, async: true

  alias CopiWeb.GameLive.Show

  describe "display_game_session/1" do
    test "returns correct labels for known editions" do
      assert Show.display_game_session("webapp") == "Cornucopia Web Session:"
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
      assert Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
      assert Show.display_game_session("unknown") == "EoP Session:"
    end
  end

  describe "latest_version/1" do
    test "returns expected version strings" do
      assert Show.latest_version("webapp") == "2.2"
      assert Show.latest_version("ecommerce") == "1.22"
      assert Show.latest_version("eop") == "5.1"
      assert Show.latest_version("other") == "1.0"
    end
  end

  describe "card_played_in_round/2" do
    test "finds card by played_in_round" do
      cards = [%{played_in_round: 1, id: "a"}, %{played_in_round: 3, id: "b"}]
      assert Show.card_played_in_round(cards, 3) == %{played_in_round: 3, id: "b"}
      assert Show.card_played_in_round(cards, 2) == nil
    end
  end

  describe "topic/1" do
    test "builds topic string" do
      assert Show.topic(42) == "game:42"
      assert Show.topic("abc") == "game:abc"
    end
  end
end
