defmodule Copi.Repo.Migrations.PopulateCards do
  use Ecto.Migration

  import Copi.CardMigration


  def change do
    add_cards_to_database(Path.join(File.cwd!, "/priv/repo/cornucopia/eop-cards-1.0-en.yaml"), nil)
    add_cards_to_database(Path.join(File.cwd!, "/../source/webapp-cards-1.22-en.yaml"), Path.join(File.cwd!, "/../source/webapp-mappings-1.22.yaml"))
  end
end
