defmodule Copi.CornucopiaLogicTest do
  use Copi.DataCase

  alias Copi.Cornucopia
  alias Copi.Cornucopia.DealtCard
  alias Copi.Repo

  setup do
    {:ok, game} = Cornucopia.create_game(%{name: "Logic Game"})
    {:ok, player1} = Cornucopia.create_player(%{name: "P1", game_id: game.id})
    {:ok, player2} = Cornucopia.create_player(%{name: "P2", game_id: game.id})
    %{game: game, p1: player1, p2: player2}
  end

  defp create_card(category, value) do
    Cornucopia.create_card(%{
      category: category, value: value,
      description: "d", misc: "m", edition: "webapp", external_id: "#{category}#{value}",
      language: "en", version: "1",
      owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [],
      capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []
    })
  end

  defp play_card(player, card, round) do
    {:ok, dealt} = Repo.insert(%DealtCard{player_id: player.id, card_id: card.id})
    {:ok, _} = Repo.update(Ecto.Changeset.change(dealt, played_in_round: round, updated_at: NaiveDateTime.utc_now() |> NaiveDateTime.truncate(:second)))
    # Sleep to ensure ordering by updated_at works if logic depends on it (it does for lead suit)
    :timer.sleep(10) 
    dealt
  end

  test "highest_scoring_card_in_round simple case", %{game: game, p1: p1, p2: p2} do
    {:ok, c1} = create_card("Cornucopia", "10") # Trump
    {:ok, c2} = create_card("Authentication", "5")
    
    # Reload game to get players
    game = Cornucopia.get_game!(game.id) |> Repo.preload(players: [dealt_cards: [:card, :votes]])

    # Both play in round 1
    # P1 leads with Authentication (if played first)
    # Wait, lead suit is determined by FIRST card played.
    d1 = play_card(p1, c2, 1) # Lead suit = Authentication
    d2 = play_card(p2, c1, 1) # Trump (Cornucopia)

    # Need votes?
    # scoring_cards filters cards with > (players-1)/2 votes.
    # players=2. (2-1)/2 = 0.5. So >0 votes.
    # So cards need at least 1 vote to score?
    
    # Let's check logic:
    # def scoring_cards(cards, number_of_players) do
    #   Enum.filter(cards, fn card -> card.played_in_round != nil && Enum.count(card.votes) > (number_of_players - 1) / 2 end)
    # end
    
    # Yes, we need votes.
    Repo.insert!(%Copi.Cornucopia.Vote{dealt_card_id: d1.id, player_id: p1.id})
    Repo.insert!(%Copi.Cornucopia.Vote{dealt_card_id: d2.id, player_id: p2.id})
    
    # Reload game structure
    game = Cornucopia.get_game!(game.id) |> Repo.preload(players: [dealt_cards: [:card, :votes]])
    
    winner = Cornucopia.highest_scoring_card_in_round(game, 1)
    
    # Cornucopia (Trump) should win over Authentication
    assert winner.id == d2.id
  end

  test "ordered_cards_played_in_round returns cards in order", %{game: game, p1: p1, p2: p2} do
    {:ok, c1} = create_card("A", "1")
    {:ok, c2} = create_card("B", "2")
    
    d1 = play_card(p1, c1, 1)
    # Manually update updated_at to be distinct (seconds)
    {:ok, d1} = Repo.update(Ecto.Changeset.change(d1, updated_at: NaiveDateTime.utc_now() |> NaiveDateTime.add(-10, :second) |> NaiveDateTime.truncate(:second)))
    
    d2 = play_card(p2, c2, 1)
    
    # Reload game to preload assoc
    game = Cornucopia.get_game!(game.id) |> Repo.preload(players: [dealt_cards: :card])
    
    cards = Cornucopia.ordered_cards_played_in_round(game, 1)
    assert Enum.count(cards) == 2
    assert List.first(cards).id == d1.id
    assert List.last(cards).id == d2.id
  end

  test "list_cards_shuffled returns cards" do
    create_card("S", "10")
    # list_cards_shuffled(edition, suits, version)
    cards = Cornucopia.list_cards_shuffled("webapp", ["S"], "1")
    assert Enum.count(cards) > 0
  end
end
