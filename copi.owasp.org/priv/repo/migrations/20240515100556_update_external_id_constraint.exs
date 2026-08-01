defmodule Copi.Repo.Migrations.UpdateExternalIdConstraint do
  use Ecto.Migration

  import Copi.CardMigration

  def change do
    drop index("cards", [:external_id])

    create unique_index("cards", [:external_id, :version])
  end
end
