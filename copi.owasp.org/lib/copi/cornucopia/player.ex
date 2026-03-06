defmodule Copi.Cornucopia.Player do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}
  @foreign_key_type Ecto.ULID

  schema "players" do
    # Encrypted at rest using AES-256-GCM via Copi.Vault (ASVS V11.3.1).
    # Decryption is transparent: callers continue to use `player.name` as before.
    field :name, Copi.Encrypted.Binary
    # Temporary migration column — holds the legacy plaintext value for records
    # that have not yet been processed by `mix copi.encrypt_names`.
    # TODO: drop after migration is confirmed complete.
    field :name_plaintext_v1, :string

    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID
    has_many :dealt_cards, Copi.Cornucopia.DealtCard

    timestamps()
  end

  def find(id) do
    case Copi.Repo.get(Copi.Cornucopia.Player, id) do
      nil ->
        {:error, :not_found}

      player ->
        {:ok,
         player
         |> Copi.Repo.preload([:game, dealt_cards: [:card, :votes]])
         |> resolve_legacy_name()}
    end
  end

  @doc """
  Backward-compatible name accessor for the transition period.

  Returns the decrypted `name` when available (post-migration), falling back to
  the plaintext `name_plaintext_v1` column for records that have not yet been
  encrypted by `mix copi.encrypt_names`.
  """
  def resolve_legacy_name(%__MODULE__{name: nil, name_plaintext_v1: legacy} = player)
      when not is_nil(legacy),
      do: %{player | name: legacy}

  def resolve_legacy_name(player), do: player

  @doc false
  def changeset(player, attrs) do
    player
    # name_plaintext_v1 is intentionally excluded from cast to prevent new writes
    # to the legacy plaintext column.  It is only written during migration setup.
    |> cast(attrs, [:name, :game_id])
    |> validate_required([:name])
    |> validate_length(:name, min: 1, max: 50)
  end
end
