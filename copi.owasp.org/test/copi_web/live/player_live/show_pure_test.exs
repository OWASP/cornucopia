defmodule CopiWeb.PlayerLive.ShowPureTest do
  use ExUnit.Case, async: true

  alias CopiWeb.PlayerLive.Show
  alias CopiWeb.PlayerLive.FormComponent

  test "topic/1 builds topic strings" do
    assert Show.topic(1) == "game:1"
    assert Show.topic("abc") == "game:abc"
  end

  test "FormComponent.topic/1 builds topic strings" do
    assert FormComponent.topic(99) == "game:99"
    assert FormComponent.topic("xyz") == "game:xyz"
  end

  test "ordered_cards/1 sorts by card.id" do
    cards = [%{card: %{id: 3}}, %{card: %{id: 1}}, %{card: %{id: 2}}]
    sorted = Show.ordered_cards(cards)
    assert Enum.map(sorted, & &1.card.id) == [1, 2, 3]
  end

  test "unplayed_cards/1 filters unplayed (0 or nil)" do
    cards = [%{played_in_round: 0, card: %{id: 1}}, %{played_in_round: nil, card: %{id: 2}}, %{played_in_round: 2, card: %{id: 3}}]
    res = Show.unplayed_cards(cards)
    assert Enum.map(res, & &1.card.id) == [1, 2]
  end

  test "played_cards/2 returns those in given round" do
    cards = [%{played_in_round: 1, card: %{id: 1}}, %{played_in_round: 2, card: %{id: 2}}]
    assert Show.played_cards(cards, 2) == [%{played_in_round: 2, card: %{id: 2}}]
  end

  test "card_played_in_round/2 finds first matching card" do
    cards = [%{played_in_round: 1, card: %{id: 1}}, %{played_in_round: 2, card: %{id: 2}}]
    assert Show.card_played_in_round(cards, 2) == %{played_in_round: 2, card: %{id: 2}}
    assert Show.card_played_in_round([], 1) == nil
  end

  test "player_first/2 places given player first" do
    players = [%{id: 2}, %{id: 1}, %{id: 3}]
    res = Show.player_first(players, %{id: 1})
    assert hd(res).id == 1
  end

  test "round_open?/1 and round_closed?/1 reflect player dealt cards" do
    # latest_round = rounds_played + 1 = 2
    # player1 has a card for round 2 -> has played
    player1 = %{id: 1, dealt_cards: [%{played_in_round: 2}]}
    # player2 has no card for round 2 -> still to play
    player2 = %{id: 2, dealt_cards: [%{played_in_round: 1}]}
    game = %{rounds_played: 1, players: [player1, player2]}

    assert Show.round_open?(game) == true
    assert Show.round_closed?(game) == false
  end

  test "last_round?/1 detects when players have no nil played_in_round" do
    # player with no nil played_in_round => they have no cards left
    player1 = %{dealt_cards: [%{played_in_round: 1}]} # no nil cards
    player2 = %{dealt_cards: [%{played_in_round: nil}]} # has nil -> still has cards
    game = %{players: [player1, player2]}

    # last_round? returns true when there is at least one player with no nil cards
    assert Show.last_round?(game) == true
  end

  test "get_vote/2 finds vote by player id" do
    votes = [%{player_id: 1, id: 10}, %{player_id: 2, id: 11}]
    dealt_card = %{votes: votes}
    player = %{id: 2}
    assert Show.get_vote(dealt_card, player) == %{player_id: 2, id: 11}
  end

  test "display_game_session/1 returns correct label for every edition" do
    assert Show.display_game_session("webapp")    == "Cornucopia Web Session:"
    assert Show.display_game_session("ecommerce") == "Cornucopia Web Session:"
    assert Show.display_game_session("mobileapp") == "Cornucopia Mobile Session:"
    assert Show.display_game_session("masvs")     == "Cornucopia Mobile Session:"
    assert Show.display_game_session("cumulus")   == "OWASP Cumulus Session:"
    assert Show.display_game_session("mlsec")     == "Elevation of MLSec Session:"
    assert Show.display_game_session("eop")       == "EoP Session:"
    assert Show.display_game_session("unknown")   == "EoP Session:"
  end
end
