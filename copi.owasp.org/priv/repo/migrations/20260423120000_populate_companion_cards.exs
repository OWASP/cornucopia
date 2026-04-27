defmodule Copi.Repo.Migrations.PopulateCompanionCards do
  use Ecto.Migration

  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/companion-cards-1.0-en.yaml"), nil)
  end
end
