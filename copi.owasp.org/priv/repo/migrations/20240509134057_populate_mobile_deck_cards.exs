defmodule Copi.Repo.Migrations.PopulateMobileDeckCards do
  use Ecto.Migration

  import Copi.CardMigration

  def change do
    migrate_cards_to_database( "priv/repo/cornucopia/masvs-cards-1.00-en.yaml", "priv/repo/cornucopia/masvs-mappings-1.0.yaml")
    migrate_cards_to_database( "priv/repo/cornucopia/masvs-cards-1.00-en.yaml", "priv/repo/cornucopia/masvs-mappings-1.0.yaml")
  end
end
