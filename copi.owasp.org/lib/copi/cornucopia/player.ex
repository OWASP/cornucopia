defmodule Copi.Cornucopia.Player do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}
  @foreign_key_type Ecto.ULID

  schema "players" do
    field :name, :string

    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID
    has_many :dealt_cards, Copi.DealtCard

    timestamps()
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name, :game_id])
    |> validate_required([:name])
  end
end
