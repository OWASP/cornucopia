defmodule Copi.Cornucopia.DealtCard do
  use Ecto.Schema
  import Ecto.Changeset

  schema "dealt_cards" do
    field :played_in_round, :integer

    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :card, Copi.Cornucopia.Card

    timestamps()
  end

  @doc false
  def changeset(dealt_card, attrs) do
    dealt_card
    |> cast(attrs, [])
    |> validate_required([])
  end
end
