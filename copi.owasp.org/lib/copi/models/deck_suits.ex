defmodule Copi.Models.DeckSuits do

  @ecommerce_suits  [
    "Data validation & encoding",
    "Authentication",
     "Session management",
    "Authorization",
    "Cryptography",
    "Cornucopia"
  ]

  def get_suits_from_deck(edition) do
    @ecommerce_suits
  end

  def get_list_of_suits_from_checkbox(game_params) do
    game_params
    |> Enum.filter(fn {_, value} -> value == "true" end)
    |> Enum.map(fn {suit_name, _} -> suit_name end)
  end

end
