defmodule Copi.Encrypted.Binary do
  @moduledoc """
  Ecto type that transparently encrypts/decrypts string values using `Copi.Vault`.

  Backed by AES-256-GCM (authenticated encryption) via the `cloak` / `cloak_ecto`
  libraries.  Values are stored as raw `bytea` in PostgreSQL.

  ## Usage

      field :name, Copi.Encrypted.Binary

  Changesets receive and return plain strings; encryption/decryption happens
  automatically at the Repo boundary (`dump/1` encrypts, `load/1` decrypts).
  This means no changes are required to changesets, validations, or templates.

  ## ASVS references
  - V11.2.1  Use industry-validated cryptographic library
  - V11.3.1  Approved mode (AES-GCM = AEAD)
  - V11.3.2  Unique IV/nonce per encryption operation (managed by Cloak)
  - V13.3.1  Secrets loaded from environment, not hardcoded
  """

  use Cloak.Ecto.Binary, vault: Copi.Vault
end
