defmodule Copi.Cornucopia.DealtCard do
  use Ecto.Schema
  import Ecto.Changeset

  schema "dealt_cards" do
    field :played_in_round, :integer
    field :scores, :boolean

    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :card, Copi.Cornucopia.Card

    has_many :votes, Copi.Cornucopia.Vote

    timestamps()
  end

  def find(id) do
    case Copi.Repo.get(Copi.Cornucopia.DealtCard, id) do
      nil -> {:error, :not_found}
      dealt_card -> {:ok, dealt_card |> Copi.Repo.preload([:card, :votes])}
    end
  end

  @doc false
  def changeset(dealt_card, attrs) do
    dealt_card
    |> cast(attrs, [])
    |> validate_required([])
  end
end
