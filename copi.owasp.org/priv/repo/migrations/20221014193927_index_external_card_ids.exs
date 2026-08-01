defmodule Copi.Repo.Migrations.IndexExternalCardIds do
  use Ecto.Migration

  def change do
    create unique_index(:cards, [:external_id])
  end
end
