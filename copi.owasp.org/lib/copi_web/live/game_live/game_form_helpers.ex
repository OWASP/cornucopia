defmodule CopiWeb.GameLive.GameFormHelpers do
  @companion_prefix "companion"
  @companion_editions ["webapp", "mobileapp"]

  def generate_suit_list_formatted_for_checkbox(edition) do
    format_list_of_suits_for_checkbox(edition)
    |> Enum.map(fn {key, _} -> key end)
  end

  def generate_selected_suits_for_new_game(edition) do
    generate_suit_list_formatted_for_checkbox(edition)
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
    |> Enum.map(fn suit -> {"#{selected_edition}-#{suit}", String.capitalize(suit)} end)
  end

  def format_companion_suits_for_checkbox(edition) when edition in @companion_editions do
    Copi.Cornucopia.get_companion_suits()
    |> Enum.map(fn suit -> {"#{@companion_prefix}-#{suit}", suit} end)
  end

  def format_companion_suits_for_checkbox(_edition), do: []

  def display_appropriate_suits_list(edition, suits) do
    selected_suits = Enum.reject(suits, &(&1 == ""))

    cond do
      selected_suits == [] ->
        generate_selected_suits_for_new_game(edition)

      Enum.any?(selected_suits, &other_edition_suit?(&1, edition)) ->
        generate_selected_suits_for_new_game(edition)

      Enum.any?(selected_suits, &String.starts_with?(&1, "#{edition}-")) ->
        suits

      edition in @companion_editions and
          Enum.all?(selected_suits, &String.starts_with?(&1, "#{@companion_prefix}-")) ->
        suits

      true ->
        generate_selected_suits_for_new_game(edition)
    end
  end

  def get_suits_from_selected_deck(assigns) do
    assigns
    |> selected_edition()
    |> format_list_of_suits_for_checkbox()
  end

  def get_companion_suits_from_selected_deck(assigns) do
    assigns
    |> selected_edition()
    |> format_companion_suits_for_checkbox()
  end

  def show_companion_suits?(assigns) do
    selected_edition(assigns) in @companion_editions
  end

  defp selected_edition(assigns) do
    if assigns.form.source.changes == nil || assigns.form.source.changes == %{} do
      "webapp"
    else
      assigns.form.source.changes.edition
    end
  end

  defp other_edition_suit?(suit, edition) do
    String.contains?(suit, "-") and
      !String.starts_with?(suit, "#{edition}-") and
      !String.starts_with?(suit, "#{@companion_prefix}-")
  end
end
