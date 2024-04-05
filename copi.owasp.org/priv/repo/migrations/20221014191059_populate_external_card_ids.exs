defmodule Copi.Repo.Migrations.PopulateExternalCardIds do
  use Ecto.Migration

  alias Copi.Repo
  alias Copi.Cornucopia.Card

  def change do
    path = Path.join(File.cwd!(), "priv/repo/cornucopia/ecommerce-cards-1.21-en.yaml")

    case YamlElixir.read_from_file(path) do
      {:ok, cards} ->
        edition = cards["meta"]["edition"]
        language = cards["meta"]["language"]
        version = cards["meta"]["version"]

        for suit <- cards["suits"] do
          for card <- suit["cards"] do
            currentCard = Repo.get_by(Card, category: suit["name"], value: card["value"])

            if currentCard do
              card
              |> Ecto.Changeset.change(external_id: card["id"])
              |> Repo.update()
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

    path = Path.join(File.cwd!(), "priv/repo/cornucopia/ecommerce-mappings-1.2.yaml")

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

            Repo.update(this_card)
          end
        end
    end
  end
end
