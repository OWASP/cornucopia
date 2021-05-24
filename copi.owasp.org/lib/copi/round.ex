defmodule Copi.Round do
  use Ecto.Schema
  import Ecto.Changeset

  schema "rounds" do
    field :number, :integer
    #field :game_id, :id
    field :winner, :id

    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID
    has_many :dealt_cards, Copi.DealtCard, foreign_key: :played_in_round

    timestamps()
  end

  @doc false
  def changeset(round, attrs) do
    round
    |> cast(attrs, [:number])
    |> validate_required([:number])
  end
end
