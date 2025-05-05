defmodule CopiWeb.GameLive.GameFormHelpers do

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game
  alias Copi.Games

  def generate_suit_list_formatted_for_checkbox(edition) do
    format_list_of_suits_for_checkbox(edition)
    |> Enum.map(fn {key, _} -> key end)
  end

  def format_suits_before_saving_game(suits) do
    regex = ~r/\A\w+-/

      suits
      |> Enum.filter(fn str -> str != "" end)
      |> Enum.map(fn suit -> String.replace(suit, regex, "") end)
  end

  def format_list_of_suits_for_checkbox(selected_edition) do
    Copi.Cornucopia.get_suits_from_selected_deck(selected_edition)
    |> Enum.sort()
    |> Enum.map(fn suit -> {"#{selected_edition}-#{suit}" , String.capitalize(suit) } end)
  end

  def display_appropriate_suits_list(edition, suits) do
    if hd(suits) == "" && length(suits) == 1 do
      generate_suit_list_formatted_for_checkbox(edition)
    else
      [_first, second | _rest] = suits
      String.contains?(second, edition)
      case String.contains?(second, edition) do
        true -> suits
        false -> generate_suit_list_formatted_for_checkbox(edition)
      end
    end
  end

  def get_suits_from_selected_deck(assigns) do
    edition = if assigns.form.source.changes == nil || assigns.form.source.changes == %{} do
      "webapp"
    else
      assigns.form.source.changes.edition
    end
    format_list_of_suits_for_checkbox(edition)
  end
end
