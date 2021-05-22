defmodule Copi.DealtCard do
  use Ecto.Schema
  import Ecto.Changeset

  schema "dealt_cards" do
    field :card_id, :id
    #field :player_id, :id
    field :played_in_round, :id

    belongs_to :player, Copi.Player

    timestamps()
  end

  @doc false
  def changeset(dealt_card, attrs) do
    dealt_card
    |> cast(attrs, [])
    |> validate_required([])
  end
end
