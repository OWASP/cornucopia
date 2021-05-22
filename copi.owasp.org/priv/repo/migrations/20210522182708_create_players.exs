defmodule Copi.Repo.Migrations.CreatePlayers do
  use Ecto.Migration

  def change do
    create table(:players) do
      add :name, :string
      add :game_id, references(:games, on_delete: :nothing)

      timestamps()
    end

    create index(:players, [:game_id])
  end
end
