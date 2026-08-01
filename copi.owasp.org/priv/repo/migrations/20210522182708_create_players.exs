defmodule Copi.Repo.Migrations.CreatePlayers do
  use Ecto.Migration

  def change do
    create table(:players, primary_key: false) do
      add :id, :binary_id, null: false, primary_key: true
      add :name, :string
      add :game_id, references(:games, type: :uuid, on_delete: :nothing)

      timestamps()
    end

    create index(:players, [:game_id])
  end
end
