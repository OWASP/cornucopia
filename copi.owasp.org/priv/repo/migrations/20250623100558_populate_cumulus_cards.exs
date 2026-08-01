defmodule Copi.Repo.Migrations.PopulateCumulusCards do
  use Ecto.Migration
  alias Copi.Repo
  alias Copi.Cornucopia
  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/cumulus-cards-1.1-en.yaml"), nil)
  end
end
