defmodule Copi.Repo.Migrations.PopulateNewCards do
  use Ecto.Migration
  alias Copi.Repo
  alias Copi.Cornucopia
  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/elevation-of-mlsec-cards-1.0-en.yaml"), Path.join(:code.priv_dir(:copi), "/repo/cornucopia/elevation-of-mlsec-mappings-1.0.yaml"))
  end
end
