defmodule Copi.Repo.Migrations.EncryptGameAndPlayerNames do
  @moduledoc """
  Migrates game.name and player.name from plaintext varchar to
  AES-256-GCM encrypted binary.
  Strategy:
    1. Add a name_encrypted binary shadow column.
    2. Read every existing plaintext row, encrypt it, write to name_encrypted.
    3. Drop the old plaintext name column.
    4. Rename name_encrypted to name.
  down/0 reverses this by decrypting back to plaintext varchar.
  """
  use Ecto.Migration
  import Ecto.Query, only: [from: 2]

  def up do
    alter table(:games) do
      add :name_encrypted, :binary
    end
    alter table(:players) do
      add :name_encrypted, :binary
    end
    flush()
    encrypt_existing_rows("games")
    encrypt_existing_rows("players")
    flush()
    alter table(:games) do
      remove :name
    end
    alter table(:players) do
      remove :name
    end
    flush()
    rename table(:games), :name_encrypted, to: :name
    rename table(:players), :name_encrypted, to: :name
  end

  def down do
    alter table(:games) do
      add :name_plaintext, :string
    end
    alter table(:players) do
      add :name_plaintext, :string
    end
    flush()
    decrypt_existing_rows("games")
    decrypt_existing_rows("players")
    flush()
    alter table(:games) do
      remove :name
    end
    alter table(:players) do
      remove :name
    end
    flush()
    rename table(:games), :name_plaintext, to: :name
    rename table(:players), :name_plaintext, to: :name
  end

  defp encrypt_existing_rows(table) do
    repo().transaction(fn ->
      from(r in ^table, where: not is_nil(r.name), select: {r.id, r.name})
      |> repo().stream(max_rows: 500)
      |> Enum.each(fn {id, plaintext} ->
        case Copi.Encrypted.Binary.encrypt(plaintext) do
          {:ok, ciphertext} ->
            repo().update_all(
              from(r in ^table, where: r.id == ^id),
              set: [name_encrypted: ciphertext]
            )
          {:error, reason} ->
            raise "Encryption failed for id=#{id}: #{inspect(reason)}"
        end
      end)
    end)
  end

  defp decrypt_existing_rows(table) do
    repo().transaction(fn ->
      from(r in ^table, where: not is_nil(r.name), select: {r.id, r.name})
      |> repo().stream(max_rows: 500)
      |> Enum.each(fn {id, ciphertext} ->
        case Copi.Encrypted.Binary.decrypt(ciphertext) do
          {:ok, plaintext} ->
            repo().update_all(
              from(r in ^table, where: r.id == ^id),
              set: [name_plaintext: plaintext]
            )
          {:error, reason} ->
            raise "Decryption failed for id=#{id}: #{inspect(reason)}"
        end
      end)
    end)
  end

end