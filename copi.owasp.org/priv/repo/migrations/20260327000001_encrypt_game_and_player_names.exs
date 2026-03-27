defmodule Copi.Repo.Migrations.EncryptGameAndPlayerNames do
  use Ecto.Migration

  def up do
    alter table(:games) do
      add :name_enc, :binary, null: true
    end

    execute "UPDATE games SET name_enc = name::bytea WHERE name IS NOT NULL"

    alter table(:games) do
      remove :name
    end

    rename table(:games), :name_enc, to: :name

    alter table(:players) do
      add :name_enc, :binary, null: true
    end

    execute "UPDATE players SET name_enc = name::bytea WHERE name IS NOT NULL"

    alter table(:players) do
      remove :name
    end

    rename table(:players), :name_enc, to: :name
  end

  def down do
    alter table(:games) do
      add :name_str, :string, null: true
    end

    execute "UPDATE games SET name_str = convert_from(name, 'UTF8') WHERE name IS NOT NULL"

    alter table(:games) do
      remove :name
    end

    rename table(:games), :name_str, to: :name

    alter table(:players) do
      add :name_str, :string, null: true
    end

    execute "UPDATE players SET name_str = convert_from(name, 'UTF8') WHERE name IS NOT NULL"

    alter table(:players) do
      remove :name
    end

    rename table(:players), :name_str, to: :name
  end
end