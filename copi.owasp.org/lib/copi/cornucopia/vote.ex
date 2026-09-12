defmodule Copi.Cornucopia.Vote do
  use Ecto.Schema
  import Ecto.Changeset

  schema "votes" do
    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :dealt_card, Copi.Cornucopia.DealtCard

    timestamps()
  end

  @doc false
  def changeset(vote, attrs) do
    vote
    |> cast(attrs, [:player_id, :dealt_card_id])
    |> validate_required([:player_id, :dealt_card_id])
    |> unique_constraint([:player_id, :dealt_card_id], name: :votes_player_id_dealt_card_id_index)
  end
end
