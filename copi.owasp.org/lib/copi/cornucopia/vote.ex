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
    |> cast(attrs, [])
    |> validate_required([])
  end
end
