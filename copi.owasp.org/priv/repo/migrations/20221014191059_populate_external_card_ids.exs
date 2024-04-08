defmodule Copi.Repo.Migrations.PopulateExternalCardIds do
  use Ecto.Migration

  import Copi.CardMigration

  def change do
    path = Path.join(File.cwd!(), "priv/repo/cornucopia/ecommerce-cards-1.21-en.yaml")
    populate_cards path

    path = Path.join(File.cwd!(), "priv/repo/cornucopia/ecommerce-mappings-1.2.yaml")
    map_cards path

    path = Path.join(File.cwd!(), "priv/repo/cornucopia/eop-cards--1.0-en.yaml")
    populate_cards path
  end
end
