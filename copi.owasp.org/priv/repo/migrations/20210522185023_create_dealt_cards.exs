defmodule Copi.Repo.Migrations.CreateDealtCards do
  use Ecto.Migration

  def change do
    create table(:dealt_cards) do
      add :card_id, references(:cards, on_delete: :nothing)
      add :player_id, references(:players, type: :uuid, on_delete: :nothing)
      add :played_in_round, references(:rounds, on_delete: :nothing)

      timestamps()
    end

    create index(:dealt_cards, [:card_id])
    create index(:dealt_cards, [:player_id])
    create index(:dealt_cards, [:played_in_round])
  end
end
