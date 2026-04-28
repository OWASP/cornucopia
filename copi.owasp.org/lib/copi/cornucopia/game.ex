defmodule Copi.Cornucopia.Game do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}

  schema "games" do
    field :created_at, :utc_datetime, default: DateTime.truncate(DateTime.utc_now(), :second)
    field :finished_at, :utc_datetime
    field :name, Copi.Encrypted.Binary
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
      nil -> {:error, :not_found}
      game -> {:ok, game |> Copi.Repo.preload([players: [dealt_cards: [:card, :votes]], continue_votes: [:player]])}
    end
  end

  @doc false
  def changeset(game, attrs) do
    game
    |> cast(attrs, [:name, :created_at, :edition, :started_at, :finished_at, :rounds_played, :suits, :round_open])
    |> validate_required([:name], message: "No really, give your game session a name")
    |> validate_format(:name, ~r/^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\uFDF2\uFDF3\uFDF4\uFDFD\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9Fー々〆〤\u3400-\u4DBF\uF900-\uFAFF\u0900-\u097F\u0621-\u064A\u0660-\u0669\u0E00-\u0E7F«»฿ฯ๏๚๛\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69FЮ́ю́Я́я́\u0370-\u03FF\u1F00-\u1FFFA-Za-zÀ-ÖØ-öø-ÿĀ-ž0-9._\--ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي ًٌٍَُِّْٰﷲﷴﷺﷻ ٠١٢٣٤٥٦٧٨٩ \s]+$/,
      message: "contains invalid characters. Only letters, numbers, spaces, and ._- are allowed.")
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
