defmodule Copi.Repo.Migrations.UpdateCardTableWithNewUrlColumAndIndex do
  use Ecto.Migration
  import Copi.CardMigration

  def change do
    drop index("cards", [:external_id, :version])
    create unique_index("cards", [:external_id, :version, :edition, :language])
    alter table(:cards) do
      Ecto.Migration.remove_if_exists :url, :string
      add :url, :string, default: ""
    end
  end
end
