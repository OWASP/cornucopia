defmodule Copi.Repo.Migrations.PopulateNewCards do
  use Ecto.Migration

  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-cards-2.00-en.yaml"), Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-mappings-2.00.yaml"))
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/mobileapp-cards-1.00-en.yaml"), Path.join(:code.priv_dir(:copi), "/repo/cornucopia/mobileapp-mappings-1.00.yaml"))
  end
end
