defmodule Copi.Repo.Migrations.CreateGames do
  use Ecto.Migration

  def change do
    create table(:games) do
      add :name, :string
      add :created_at, :utc_datetime
      add :started_at, :utc_datetime
      add :finished_at, :utc_datetime

      timestamps()
    end

  end
end
