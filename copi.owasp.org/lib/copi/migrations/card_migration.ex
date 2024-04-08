defmodule Copi.CardMigration do
  alias Copi.Repo
  alias Copi.Cornucopia.Card

  def populate_cards(path) do
    case YamlElixir.read_from_file(path) do
      {:ok, cards} ->
        edition = cards["meta"]["edition"]
        language = cards["meta"]["language"]
        version = cards["meta"]["version"]
        for suit <- cards["suits"] do
          for card <- suit["cards"] do
            this_card = Repo.get_by(Card, category: suit["name"], value: card["value"])

            if this_card do
              update_card(card: card)
            else
              misc = if Map.has_key?(card, "misc"), do: card["misc"], else: ""

              Repo.insert!(%Card{
                edition: edition,
                language: language,
                version: version,
                category: suit["name"],
                value: card["value"],
                description: card["desc"],
                misc: misc
              })
            end
          end
        end
    end
  end


  def update_card(card)do
    card
    |> Ecto.Changeset.change(external_id: card["id"])
    |> Repo.update()
  end

  def map_cards(path) do
    case YamlElixir.read_from_file(path) do
      {:ok, cards} ->
        for suit <- cards["suits"] do
          for card <- suit["cards"] do
            this_card = Repo.get_by!(Card, category: suit["name"], value: card["value"])

            this_card =
              Ecto.Changeset.change(this_card,
                owasp_scp: Enum.map(card["owasp_scp"], fn x -> to_string(x) end),
                owasp_asvs: Enum.map(card["owasp_asvs"], fn x -> to_string(x) end),
                owasp_appsensor: Enum.map(card["owasp_appsensor"], fn x -> to_string(x) end),
                capec: Enum.map(card["capec"], fn x -> to_string(x) end),
                safecode: Enum.map(card["safecode"], fn x -> to_string(x) end)
              )

            Repo.update this_card
          end
        end
    end
  end
end
