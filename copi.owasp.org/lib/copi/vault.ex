defmodule Copi.Vault do
  @moduledoc """
  Application-level encryption vault using AES-256-GCM (authenticated encryption).

  The vault is configured via the `:copi, Copi.Vault` application config, which
  must supply a 32-byte AES key loaded from the `COPI_ENCRYPTION_KEY` environment
  variable in production (see `config/runtime.exs`).

  ## Key rotation

  To rotate the encryption key, add the old cipher(s) as additional entries in the
  `:ciphers` list (without the `default:` label). Cloak will try each cipher in
  order when decrypting, allowing all existing records to be read while new writes
  use the current default key. Run `mix copi.encrypt_names` after rotation to
  re-encrypt all records with the new key.

  ## Key generation

      $ mix phx.gen.secret 32 | base64
      # or
      $ openssl rand -base64 32

  The exported value is what you set as `COPI_ENCRYPTION_KEY`.
  """

  use Cloak.Vault, otp_app: :copi
end
