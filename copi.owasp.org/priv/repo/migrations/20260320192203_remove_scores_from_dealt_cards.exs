defmodule Copi.Repo.Migrations.RemoveScoresFromDealtCards do
  use Ecto.Migration

  def change do
    alter table(:dealt_cards) do
      remove :scores, :boolean
    end
  end
end
