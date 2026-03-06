defmodule Copi.Repo.Migrations.EncryptGameAndPlayerNames do
  @moduledoc """
  Adds encrypted `name` (bytea) columns to `games` and `players`, and renames
  the existing plaintext `name` (varchar) columns to `name_plaintext_v1` so that
  legacy data is preserved during the transition period.

  ## Deployment procedure

  After running this migration, execute the data-migration task to encrypt all
  existing records:

      $ mix copi.encrypt_names

  Once every record has a non-NULL `name` (encrypted), the `name_plaintext_v1`
  column can be dropped in a follow-up migration.
  """

  use Ecto.Migration

  def up do
    # Preserve existing plaintext values under a legacy column name.
    # This lets the application fall back gracefully for any record that has
    # not yet been processed by `mix copi.encrypt_names`.
    rename table(:games), :name, to: :name_plaintext_v1
    rename table(:players), :name, to: :name_plaintext_v1

    # Add the new encrypted binary columns (nullable during migration window).
    alter table(:games) do
      add :name, :binary
    end

    alter table(:players) do
      add :name, :binary
    end
  end

  def down do
    alter table(:games) do
      remove :name
    end

    alter table(:players) do
      remove :name
    end

    rename table(:games), :name_plaintext_v1, to: :name
    rename table(:players), :name_plaintext_v1, to: :name
  end
end
