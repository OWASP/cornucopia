defmodule Copi.Repo.Migrations.PopulateNewCards do
  use Ecto.Migration
  alias Copi.Repo
  alias Copi.Cornucopia
  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/eop-cards-5.0-en.yaml"), nil)
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-cards-2.1-en.yaml"), Path.join(:code.priv_dir(:copi), "/repo/cornucopia/webapp-mappings-2.1.yaml"))
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/mobileapp-cards-1.1-en.yaml"), Path.join(:code.priv_dir(:copi), "/repo/cornucopia/mobileapp-mappings-1.1.yaml"))
  end
end
