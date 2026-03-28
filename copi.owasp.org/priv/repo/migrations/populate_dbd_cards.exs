defmodule Copi.Repo.Migrations.PopulateDbdCards do
  use Ecto.Migration

  import Copi.CardMigration


  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/dbd-cards-1.0-en.yaml"), nil)
  end
end
