defmodule Mix.Tasks.Copi.EncryptNames do
  @moduledoc """
  Encrypts legacy plaintext `name_plaintext_v1` values for all `games` and
  `players` that have not yet been migrated to the encrypted `name` column.

  ## Usage

      mix copi.encrypt_names

  Run this task **once** immediately after deploying the
  `EncryptGameAndPlayerNames` migration.  It is safe to run multiple times;
  only records whose `name` column is still NULL are processed.

  ## What it does

  1. Queries all games / players where `name IS NULL AND name_plaintext_v1 IS NOT NULL`.
  2. Re-saves each record via its Ecto changeset, which triggers
     `Copi.Encrypted.Binary.dump/1` and writes the AES-GCM ciphertext into `name`.
  3. Logs progress to stdout.

  ## After migration

  Once this task reports 0 remaining records, the `name_plaintext_v1` column
  can be dropped in a follow-up migration.
  """

  use Mix.Task

  @shortdoc "Backfills encrypted names for legacy game and player records"

  @impl Mix.Task
  def run(_args) do
    # Ensure the OTP application (and therefore Copi.Vault) is started.
    Mix.Task.run("app.start")

    alias Copi.Repo
    alias Copi.Cornucopia.{Game, Player}
    import Ecto.Query, only: [from: 2]

    encrypt_records(Repo, Game, "games")
    encrypt_records(Repo, Player, "players")

    Mix.shell().info("Done. All eligible records have been encrypted.")
  end

  # ---------------------------------------------------------------------------
  # Private helpers
  # ---------------------------------------------------------------------------

  defp encrypt_records(repo, schema, label) do
    pending =
      repo.all(
        from r in schema,
          where: is_nil(r.name) and not is_nil(r.name_plaintext_v1)
      )

    Mix.shell().info("Encrypting #{length(pending)} #{label}...")

    Enum.each(pending, fn record ->
      record
      |> schema.changeset(%{name: record.name_plaintext_v1})
      |> repo.update!()
    end)
  end
end
