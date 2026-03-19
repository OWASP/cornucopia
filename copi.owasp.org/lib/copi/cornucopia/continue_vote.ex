defmodule Copi.Cornucopia.ContinueVote do
  use Ecto.Schema
  import Ecto.Changeset

  schema "continue_votes" do
    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID

    timestamps()
  end

  @doc false
  def changeset(continue_vote, attrs) do
    continue_vote
    |> cast(attrs, [:player_id, :game_id])
    |> validate_required([:player_id, :game_id])
    |> unique_constraint([:player_id, :game_id], name: :continue_votes_player_id_game_id_index)
  end
end