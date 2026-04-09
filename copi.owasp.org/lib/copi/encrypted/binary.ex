defmodule Copi.Encrypted.Binary do
  @moduledoc """
  Custom Ecto type that encrypts/decrypts values using AES-256-GCM.
  Key is loaded from COPI_ENCRYPTION_KEY env var first, then application config.
  Stored as binary in the database.
  """

  use Ecto.Type

  @magic_prefix "ENC1"
  @iv_bytes 12
  @tag_bytes 16

  @impl Ecto.Type
  def type, do: :binary

  @impl Ecto.Type
  def cast(value) when is_binary(value), do: {:ok, value}
  def cast(_), do: :error

  @impl Ecto.Type
  def dump(nil), do: {:ok, nil}
  def dump(value) when is_binary(value) do
    case encrypt(value) do
      {:ok, blob} -> {:ok, blob}
      {:error, reason} -> raise "Copi.Encrypted.Binary dump/1 failed: #{reason}"
    end
  end
  def dump(_), do: :error

  @impl Ecto.Type
  def load(nil), do: {:ok, nil}
  def load(value) when is_binary(value) do
    case decrypt(value) do
      {:ok, plaintext} -> {:ok, plaintext}
      {:error, :not_encrypted} -> {:ok, value}
      {:error, reason} -> raise "Copi.Encrypted.Binary load/1 failed: #{reason}"
    end
  end
  def load(_), do: :error

  def encrypt(plaintext) when is_binary(plaintext) do
    with {:ok, key} <- fetch_key() do
      iv = :crypto.strong_rand_bytes(@iv_bytes)
      {ciphertext, tag} =
        :crypto.crypto_one_time_aead(:aes_256_gcm, key, iv, plaintext, @magic_prefix, true)
      blob = @magic_prefix <> iv <> tag <> ciphertext
      {:ok, blob}
    end
  end

  def decrypt(blob) when is_binary(blob) do
    case blob do
      <<@magic_prefix, iv::binary-size(@iv_bytes), tag::binary-size(@tag_bytes),
        ciphertext::binary>> ->
        with {:ok, key} <- fetch_key() do
          case :crypto.crypto_one_time_aead(
                 :aes_256_gcm, key, iv, ciphertext, @magic_prefix, tag, false
               ) do
            :error -> {:error, "AES-GCM authentication failed"}
            plaintext -> {:ok, plaintext}
          end
        end
      _ ->
        {:error, :not_encrypted}
    end
  end

  defp fetch_key do
    raw =
      System.get_env("COPI_ENCRYPTION_KEY") ||
        Application.get_env(:copi, :encryption_key) ||
        raise "COPI_ENCRYPTION_KEY is not set"

    key = Base.decode64!(String.trim(raw))

    if byte_size(key) != 32 do
      raise ArgumentError,
            "COPI_ENCRYPTION_KEY must decode to exactly 32 bytes, got #{byte_size(key)}"
    end

    {:ok, key}
  end
end