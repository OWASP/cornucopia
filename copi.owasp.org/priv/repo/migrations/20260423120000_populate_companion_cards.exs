defmodule Copi.Repo.Migrations.PopulateCompanionCards do
  use Ecto.Migration

  import Copi.CardMigration

  @cards_file Path.join(:code.priv_dir(:copi), "repo/cornucopia/companion-cards-1.0-en.yaml")

  def up do
    add_cards_to_database(@cards_file, nil)
  end

  def down do
    # ASVS V2.3: use explicit migration direction for non-reversible data changes.
    # Replace this with a scoped delete for the rows inserted by `up/0` once the
    # target table/identifier columns are known in this migration context.
    raise "Irreversible rollback: implement deletion for cards loaded from #{@cards_file}"
  end
end
