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
                  <% score = player.dealt_cards |> Copi.Cornucopia.scoring_cards(Enum.count(@game.players)) |> Enum.count %>
                  <% highest_card_bonus = player |> Copi.Cornucopia.highest_scoring_cards_for_player(@game) |> Enum.count %>
                  <tr>
                    <td class="whitespace-nowrap py-5 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6"><%= player.name %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-3.5 text-sm text-gray-500"><%= player.dealt_cards |> Copi.Cornucopia.unplayed_cards |> Enum.count %></td>
                      <td  class="text-right whitespace-nowrap px-3 py-4 text-sm text-gray-500"><%= player.dealt_cards |> Copi.Cornucopia.played_cards |> Enum.count %></td>
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
end
