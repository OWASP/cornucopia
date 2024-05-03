defmodule Copi.Repo.Migrations.CreateGames do
  use Ecto.Migration

  def change do
    create table(:games, primary_key: false) do
      add :id, :binary_id, null: false, primary_key: true
      add :name, :string
      add :created_at, :utc_datetime
      add :started_at, :utc_datetime
      add :finished_at, :utc_datetime
      add :rounds_played, :integer, default: 0

      timestamps()
    end
  end
end
