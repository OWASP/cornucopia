defmodule Copi.CardMigration do
  alias Copi.Repo
  alias Copi.Cornucopia.Card

  def add_cards_to_database(cards_file_path, mappings_file_path)do
    populate_cards Path.join(File.cwd!(), cards_file_path)

    if(mappings_file_path) do
      map_cards Path.join(File.cwd!(), mappings_file_path)
    end
  end

  defp populate_cards(path) do
    case YamlElixir.read_from_file(path) do
      {:ok, cards} ->
        edition = cards["meta"]["edition"]
        language = cards["meta"]["language"]
        version = cards["meta"]["version"]
        for suit <- cards["suits"] do
          for card <- suit["cards"] do
            card_exists = Repo.get_by(Card, category: suit["name"], value: card["value"], edition: edition, language: language)

            if card_exists  do
                # nothing
            else
              misc = if Map.has_key?(card, "misc"), do: card["misc"], else: ""

              Repo.insert!(%Card{
                edition: edition,
                language: language,
                version: version,
                category: suit["name"],
                value: card["value"],
                description: card["desc"],
                misc: misc,
                external_id: card["id"]
              })
            end
          end
        end
    end
  end


  defp map_cards(path) do
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
                  owasp_masvs: [],
                  owasp_mastg: [],
                  owasp_appsensor: set_mappings_for_card(card["owasp_appsensor"]),
                  capec: set_mappings_for_card(card["capec"]),
                  safecode: set_mappings_for_card(card["safecode"])
                )
                "masvs" -> Ecto.Changeset.change(this_card,
                owasp_scp: [],
                owasp_asvs: [],
                owasp_masvs: set_mappings_for_card(card["owasp_masvs"]),
                owasp_mastg: set_mappings_for_card(card["owasp_mastg"]),
                owasp_appsensor: [],
                capec: set_mappings_for_card(card["capec"]),
                safecode: set_mappings_for_card(card["safecode"])
                )
            end
            Repo.update this_card
          end
        end
    end
  end

  defp set_mappings_for_card(mappings) do
    mappings |> Enum.map(fn x -> to_string(x) end)
  end
end
