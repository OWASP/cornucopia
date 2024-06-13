defmodule CopiWeb.GameComponents do
  @moduledoc """
  Provides game UI components.
  """
  use Phoenix.Component

  @doc """
  Renders a game's current scoring situation.
  """
  attr :id, :string, required: true
  attr :game, :map, required: true
  def game_scores(assigns) do
    ~H"""
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Name</th>
                  <th scope="col" class="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Cards</th>
                  <th scope="col" class="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Played</th>
                  <th scope="col" class="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Score</th>
                  <th scope="col" class="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Highest Card Bonus</th>
                  <th scope="col" class="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Total Score</th>
                </tr>
              </thead>
              <tbody id="players" class="divide-y divide-gray-200 bg-white">
                <%= for {player, _index} <- Enum.with_index(@game.players) do %>
                  <% score = player.dealt_cards |> scoring_cards(Enum.count(@game.players)) |> Enum.count %>
                  <% highest_card_bonus = player |> highest_scoring_cards(@game) |> Enum.count %>
                  <tr>
                    <td class="whitespace-nowrap py-5 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6"><%= player.name %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-3.5 text-sm text-gray-500"><%= player.dealt_cards |> unplayed_cards |> Enum.count %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-4 text-sm text-gray-500"><%= player.dealt_cards |> played_cards |> Enum.count %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-4 text-sm text-gray-500"><%= score %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-4 text-sm text-gray-500"><%= highest_card_bonus %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-4 text-sm text-gray-500"><strong><%= score + highest_card_bonus %></strong></td>
                  </tr>
                <% end %>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    """
  end

  defp highest_scoring_cards(player, game) do

    Enum.reduce(game.players, [], fn player, cards -> (player.dealt_cards |> played_cards) ++ cards end) # Combine all played cards from all players
      |> lead_suit_cards # Filter to just the lead suit cards
      |> scoring_cards(Enum.count(game.players)) # Filter to just the cards that scored
      |> Enum.group_by(fn card -> card.played_in_round end) # Convert to map where {round, [scoring_cards]}
      |> Enum.flat_map(fn {_, cards} -> highest_scoring_cards(cards) end) # Back to a list of just the highest scoring card in each round
      |> Enum.filter(fn dealt_card -> dealt_card.player_id == player.id end) # Filter out just the highest scoring cards for the player provided

  end

  defp highest_scoring_cards(cards) do
    card_order = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "JokerB", "JokerA"]

    Enum.group_by(cards, fn dealt_card -> Enum.find_index(card_order, fn value -> value == dealt_card.card.value end) end)
      |> Enum.max_by(fn {index, _cards} -> index end)
      |> elem(1)
  end

  defp unplayed_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round == nil end)
  end

  defp played_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round != nil end)
  end

  defp scoring_cards(cards, number_of_players) do
    Enum.filter(cards, fn card -> card.played_in_round != nil && Enum.count(card.votes) > (number_of_players - 1) / 2 end)
  end

  defp lead_suit_cards(cards) do
    Enum.group_by(cards, fn card -> card.played_in_round end) # Convert to map where {round, [played_cards]}
      |> Map.new(fn {round, played_cards} -> {round, Enum.sort_by(played_cards, &(&1.updated_at))} end) # Sort played cards in rounds by when played
      |> Enum.flat_map(fn {_round, ordered_played_cards} -> Enum.filter(ordered_played_cards, fn card -> card.card.category == List.first(ordered_played_cards).card.category or card.card.value in ["JokerA", "JokerB"] or String.upcase(card.card.category) == "CORNUCOPIA" end) end) # Back to a list of just the lead suit cards in each round (plus jokers and trump cards)
  end
end
