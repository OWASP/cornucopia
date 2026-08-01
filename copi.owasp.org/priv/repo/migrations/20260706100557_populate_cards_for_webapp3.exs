defmodule Copi.Repo.Migrations.PopulateNewCardsForWebApp3 do
  use Ecto.Migration
  alias Copi.Repo
  alias Copi.Cornucopia
  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-cards-3.0-en.yaml"), nil)
  end
end
