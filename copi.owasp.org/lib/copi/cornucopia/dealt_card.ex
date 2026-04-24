defmodule Copi.Cornucopia.DealtCard do
  use Ecto.Schema
  import Ecto.Changeset

  schema "dealt_cards" do
    field :played_in_round, :integer

    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :card, Copi.Cornucopia.Card

    has_many :votes, Copi.Cornucopia.Vote

    timestamps()
  end

  def find(id) when is_binary(id) do
    case Integer.parse(id) do
      {int_id, ""} -> find(int_id)
      _ -> {:error, :invalid_id}
    end
  end

  def find(id) when is_integer(id) do
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
