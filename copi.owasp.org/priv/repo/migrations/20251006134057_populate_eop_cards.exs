defmodule Copi.Repo.Migrations.PopulateEopCards do
  use Ecto.Migration

  import Copi.CardMigration


  def change do
    add_cards_to_database(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/eop-cards-5.1-en.yaml"), nil)
  end
end
