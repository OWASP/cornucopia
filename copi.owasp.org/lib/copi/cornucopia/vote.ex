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
    |> cast(attrs, [:dealt_card_id, :player_id])
    |> validate_required([:dealt_card_id, :player_id])
  end
end
