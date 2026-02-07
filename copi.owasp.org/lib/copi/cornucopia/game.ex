defmodule Copi.Cornucopia.Game do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}

  schema "games" do
    field :created_at, :utc_datetime, default: DateTime.truncate(DateTime.utc_now(), :second)
    field :finished_at, :utc_datetime
    field :name, :string
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
