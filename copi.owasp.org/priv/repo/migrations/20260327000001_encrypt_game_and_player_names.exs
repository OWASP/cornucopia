defmodule Copi.Repo.Migrations.EncryptGameAndPlayerNames do
  @moduledoc """
  Migrates game.name and player.name from plaintext varchar to
  AES-256-GCM encrypted binary.
  """
  use Ecto.Migration
  import Ecto.Query

  def up do
    alter table(:games) do
      add :name_encrypted, :binary
    end
    alter table(:players) do
      add :name_encrypted, :binary
    end
    flush()
    encrypt_existing_rows(:games)
    encrypt_existing_rows(:players)
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
    decrypt_existing_rows(:games)
    decrypt_existing_rows(:players)
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

  defp encrypt_existing_rows(table_name) do
    repo().transaction(fn ->
      rows =
        repo().all(
          from r in {to_string(table_name), Copi.Encrypted.Row},
          where: not is_nil(r.name),
          select: {r.id, r.name}
        )

      Enum.each(rows, fn {id, plaintext} ->
        case Copi.Encrypted.Binary.encrypt(plaintext) do
          {:ok, ciphertext} ->
            repo().query!(
              "UPDATE #{table_name} SET name_encrypted = $1 WHERE id = $2",
              [ciphertext, id]
            )
          {:error, reason} ->
            raise "Encryption failed for id=#{id}: #{inspect(reason)}"
        end
      end)
    end)
  end

  defp decrypt_existing_rows(table_name) do
    repo().transaction(fn ->
      {:ok, %{rows: rows}} =
        repo().query("SELECT id, name FROM #{table_name} WHERE name IS NOT NULL")

      Enum.each(rows, fn [id, ciphertext] ->
        case Copi.Encrypted.Binary.decrypt(ciphertext) do
          {:ok, plaintext} ->
            repo().query!(
              "UPDATE #{table_name} SET name_plaintext = $1 WHERE id = $2",
              [plaintext, id]
            )
          {:error, reason} ->
            raise "Decryption failed for id=#{id}: #{inspect(reason)}"
        end
      end)
    end)
  end

end