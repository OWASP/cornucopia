defmodule Copi.Cornucopia.Player do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}
  @foreign_key_type Ecto.ULID

  schema "players" do
    field :name, :string

    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID
    has_many :dealt_cards, Copi.Cornucopia.DealtCard

    timestamps()
  end

  def find(id) do
    case Copi.Repo.get(Copi.Cornucopia.Player, id) do
      nil -> {:error, :not_found}
      player -> {:ok, player |> Copi.Repo.preload([:game, dealt_cards: [:card]])}
    end
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name, :game_id])
    |> validate_required([:name])
  end
end
