defmodule Copi.Repo.Migrations.CreateSecuritySessionTables do
  use Ecto.Migration

  def change do
    create table(:copi_sessions, primary_key: false) do
      add :id, :string, primary_key: true
      add :data, :binary, null: false
      add :expires_at, :utc_datetime_usec, null: false
    end

    create index(:copi_sessions, [:expires_at])

    create table(:player_capability_consumptions, primary_key: false) do
      add :digest, :binary, primary_key: true
      add :expires_at, :utc_datetime_usec, null: false
    end

    create index(:player_capability_consumptions, [:expires_at])
  end
end
