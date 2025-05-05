defmodule Copi.Repo.Migrations.PopulateNewCards do
  use Ecto.Migration
  alias Copi.Repo
  alias Copi.Cornucopia
  import Copi.CardMigration

  def change do
    add_cards_to_database(Path.join(File.cwd!, "/../source/eop-cards-5.0-en.yaml"), nil)
    add_cards_to_database(Path.join(File.cwd!, "/../source/webapp-cards-2.1-en.yaml"), Path.join(File.cwd!, "/../source/webapp-mappings-2.1.yaml"))
    add_cards_to_database(Path.join(File.cwd!, "/../source/mobileapp-cards-1.1-en.yaml"), Path.join(File.cwd!, "/../source/mobileapp-mappings-1.1.yaml"))
  end
end
