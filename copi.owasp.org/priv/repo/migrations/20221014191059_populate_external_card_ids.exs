defmodule Copi.Repo.Migrations.PopulateExternalCardIds do
  use Ecto.Migration

  alias Copi.Repo
  alias Copi.Cornucopia.Card

  def change do
    path = Path.join(File.cwd!(), "priv/repo/cornucopia/ecommerce-cards-1.21-en.yaml")

    case YamlElixir.read_from_file(path) do
      {:ok, cards} ->
        for suit <- cards["suits"] do
          for card <- suit["cards"] do
             Repo.get_by!(Card, [category: suit["name"], value: card["value"]])
            |> Ecto.Changeset.change(external_id: card["id"])
            |> Repo.update()
          end
        end
    end

    path = Path.join(File.cwd!(), "priv/repo/cornucopia/eop-cards--1.0-en.yaml")

    case YamlElixir.read_from_file(path) do
      {:ok, cards} ->
        for suit <- cards["suits"] do
          for card <- suit["cards"] do
             Repo.get_by!(Card, [category: suit["name"], value: card["value"]])
            |> Ecto.Changeset.change(external_id: card["id"])
            |> Repo.update()
          end
        end
    end
  end
end
