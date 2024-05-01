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

            if this_card && this_card.edition == edition  do
                update_card(card)
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
        edition = cards["meta"]["edition"]
        for suit <- cards["suits"] do
          for card <- suit["cards"] do
            this_card = Repo.get_by!(Card, category: suit["name"], value: card["value"], edition: edition)

            this_card =  case edition do
             "ecommerce" -> Ecto.Changeset.change(this_card,
                  owasp_scp: set_mappings_for_card(card["owasp_scp"]),
                  owasp_asvs: set_mappings_for_card(card["owasp_asvs"]),
                  owasp_masvs: nil,
                  owasp_mastg: nil,
                  owasp_appsensor: set_mappings_for_card(card["owasp_appsensor"]),
                  capec: set_mappings_for_card(card["capec"]),
                  safecode: set_mappings_for_card(card["safecode"])
                )
                "masvs" -> Ecto.Changeset.change(this_card,
                owasp_scp: nil,
                owasp_asvs: nil,
                owasp_masvs: set_mappings_for_card(card["owasp_masvs"]),
                owasp_mastg: set_mappings_for_card(card["owasp_mastg"]),
                owasp_appsensor: nil,
                capec: set_mappings_for_card(card["capec"]),
                safecode: set_mappings_for_card(card["safecode"])
                )
            end
            Repo.update this_card
          end
        end
    end
  end

  def set_mappings_for_card(mappings) do
    mappings |> Enum.map(fn x -> to_string(x) end)
  end

  def migrate_cards_to_database(cards_file_path, mappings_file_path)do
    populate_cards Path.join(File.cwd!(), cards_file_path)

    if(mappings_file_path) do
      map_cards Path.join(File.cwd!(), mappings_file_path)
    end
  end

end
