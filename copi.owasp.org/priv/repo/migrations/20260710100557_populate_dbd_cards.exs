defmodule Copi.Repo.Migrations.PopulateDbdCards do
  use Ecto.Migration

  import Copi.CardMigration

  @cards_file Path.join(:code.priv_dir(:copi), "repo/cornucopia/dbd-cards-1.0-en.yaml")

  def up do
    add_cards_to_database(@cards_file, nil)
  end

  def down do
    raise "Irreversible rollback: implement deletion for cards loaded from #{@cards_file}"
  end
end