defmodule Copi.Repo.Migrations.PopulateNewCards do
  use Ecto.Migration

  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(File.cwd!, "/../source/webapp-cards-2.0-en.yaml"), Path.join(File.cwd!, "/../source/webapp-mappings-2.0.yaml"))
    add_cards_to_database(Path.join(File.cwd!, "/../source/mobileapp-cards-1.0-en.yaml"), Path.join(File.cwd!, "/../source/mobileapp-mappings-1.0.yaml"))
  end
end
