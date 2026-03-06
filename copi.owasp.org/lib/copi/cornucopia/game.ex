defmodule Copi.Cornucopia.Game do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}

  schema "games" do
    field :created_at, :utc_datetime, default: DateTime.truncate(DateTime.utc_now(), :second)
    field :finished_at, :utc_datetime
    # Encrypted at rest using AES-256-GCM via Copi.Vault (ASVS V11.3.1).
    # Decryption is transparent: callers continue to use `game.name` as before.
    field :name, Copi.Encrypted.Binary
    # Temporary migration column — holds the legacy plaintext value for records
    # that have not yet been processed by `mix copi.encrypt_names`.
    # TODO: drop after migration is confirmed complete.
    field :name_plaintext_v1, :string
    field :edition, :string
    field :started_at, :utc_datetime
    field :rounds_played, :integer, default: 0
    field :suits, {:array, :string}, default: []
    field :round_open, :boolean, default: true

    has_many :players, Copi.Cornucopia.Player
    has_many :continue_votes, Copi.Cornucopia.ContinueVote

    timestamps()
  end

  def find(id) do
    case Copi.Repo.get(Copi.Cornucopia.Game, id) do
      nil ->
        {:error, :not_found}

      game ->
        game =
          game
          |> Copi.Repo.preload(players: [dealt_cards: [:card, :votes]], continue_votes: [:player])
          |> resolve_legacy_name()
          |> Map.update!(:players, fn players ->
            Enum.map(players, &Copi.Cornucopia.Player.resolve_legacy_name/1)
          end)

        {:ok, game}
    end
  end

  @doc """
  Backward-compatible name accessor for the transition period.

  Returns the decrypted `name` when available (post-migration), falling back to
  the plaintext `name_plaintext_v1` column for records that have not yet been
  encrypted by `mix copi.encrypt_names`.
  """
  def resolve_legacy_name(%__MODULE__{name: nil, name_plaintext_v1: legacy} = game)
      when not is_nil(legacy),
      do: %{game | name: legacy}

  def resolve_legacy_name(game), do: game

  @doc false
  def changeset(game, attrs) do
    game
    # name_plaintext_v1 is intentionally excluded from cast to prevent new writes
    # to the legacy plaintext column.  It is only written during migration setup.
    |> cast(attrs, [:name, :created_at, :edition, :started_at, :finished_at, :rounds_played, :suits, :round_open])
    |> validate_required([:name], message: "No really, give your game session a name")
  end

  def continue_vote_count(game) do
    Enum.count(game.continue_votes)
  end

  def has_continue_vote?(game, player) do
    Enum.any?(game.continue_votes, fn vote -> vote.player_id == player.id end)
  end

  def majority_continue_votes_reached?(game) do
    total_players = Enum.count(game.players)
    continue_votes = continue_vote_count(game)
    
    continue_votes > div(total_players, 2)
  end

  def can_continue_round?(game) do
    round_open?(game) and majority_continue_votes_reached?(game)
  end

  def round_open?(game) do
    latest_round = game.rounds_played + 1

    players_still_to_play = game.players |> Enum.filter(fn player -> 
      Enum.find(player.dealt_cards, fn card -> card.played_in_round == latest_round end) == nil 
    end)

    Enum.count(players_still_to_play) > 0
  end
end
