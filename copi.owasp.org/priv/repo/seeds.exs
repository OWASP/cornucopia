# Script for populating the database. You can run it as:
#
#     mix run priv/repo/seeds.exs
#
# Inside the script, you can read and write to any of your
# repositories directly:
#
#     Copi.Repo.insert!(%Copi.SomeSchema{})
#
# We recommend using the bang functions (`insert!`, `update!`
# and so on) as they will fail if something goes wrong.

alias Copi.Repo
alias Copi.Card

path = Path.join(File.cwd!(), "priv/repo/cornucopia/ecommerce-cards-1.21-en.yaml")

case YamlElixir.read_from_file(path) do
  {:ok, cards} ->
    edition = cards["meta"]["edition"]
    language = cards["meta"]["language"]
    version = cards["meta"]["version"]

    for suit <- cards["suits"] do
      for card <- suit["cards"] do
        misc = if Map.has_key?(card, "misc"), do: card["misc"], else: ""

        Repo.insert! %Card{
          edition: edition,
          language: language,
          version: version,
          category: suit["name"],
          value: card["value"],
          description: card["desc"],
          misc: misc
        }
      end
    end
end
