defmodule Copi.Player do
  use Ecto.Schema
  import Ecto.Changeset

  schema "players" do
    field :name, :string
    #field :game_id, :id

    belongs_to :game, Copi.Game
    has_many :dealt_cards, Copi.DealtCard

    timestamps()
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name])
    |> validate_required([:name])
  end
end
