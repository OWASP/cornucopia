defmodule Copi.Repo.Migrations.CreateVotes do
  use Ecto.Migration

  def change do
    create table(:votes) do
      add :player_id, references(:players, type: :uuid, on_delete: :nothing)
      add :dealt_card_id, references(:dealt_cards, on_delete: :nothing)

      timestamps()
    end

    create index(:votes, [:player_id])
    create index(:votes, [:dealt_card_id])
  end
end
