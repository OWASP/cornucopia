defmodule Copi.Repo.Migrations.PopulateCards do
  use Ecto.Migration

  import Copi.CardMigration


  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/eop-cards-1.0-en.yaml"), nil)
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-cards-1.22-en.yaml"), Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-mappings-1.22.yaml"))
  end
end
