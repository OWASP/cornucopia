defmodule CopiWeb.GameLive.ShowHelpersTest do
  use ExUnit.Case, async: true
  alias CopiWeb.GameLive.Show

  describe "display_game_session/1" do
    test "webapp returns web session" do
      assert Show.display_game_session("webapp") == "Cornucopia Web Session:"
    end
    test "ecommerce returns web session" do
      assert Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
    end
    test "mobileapp returns mobile session" do
      assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
    end
    test "mlsec returns MLSec session" do
      assert Show.display_game_session("mlsec") == "Elevation of MLSec Session:"
    end
    test "cumulus returns Cumulus session" do
      assert Show.display_game_session("cumulus") == "OWASP Cumulus Session:"
    end
    test "masvs returns mobile session" do
      assert Show.display_game_session("masvs") == "Cornucopia Mobile Session:"
    end
    test "unknown returns EoP session" do
      assert Show.display_game_session("unknown") == "EoP Session:"
    end
  end

  describe "latest_version/1" do
    test "webapp" do assert Show.latest_version("webapp") == "2.2" end
    test "ecommerce" do assert Show.latest_version("ecommerce") == "1.22" end
    test "mobileapp" do assert Show.latest_version("mobileapp") == "1.1" end
    test "mlsec" do assert Show.latest_version("mlsec") == "1.0" end
    test "cumulus" do assert Show.latest_version("cumulus") == "1.1" end
    test "masvs" do assert Show.latest_version("masvs") == "1.1" end
    test "eop" do assert Show.latest_version("eop") == "5.1" end
    test "unknown defaults to 1.0" do assert Show.latest_version("other") == "1.0" end
  end

  describe "card_played_in_round/2" do
    test "finds card played in given round" do
      cards = [
        %{played_in_round: 1, id: 1},
        %{played_in_round: 2, id: 2}
      ]
      assert Show.card_played_in_round(cards, 1) == %{played_in_round: 1, id: 1}
    end

    test "returns nil if no card in round" do
      cards = [%{played_in_round: 1, id: 1}]
      assert Show.card_played_in_round(cards, 5) == nil
    end

    test "returns nil for empty list" do
      assert Show.card_played_in_round([], 1) == nil
    end
  end
end