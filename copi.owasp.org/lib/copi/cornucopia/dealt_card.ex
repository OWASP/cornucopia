defmodule Copi.Cornucopia.DealtCard do
  use Ecto.Schema
  import Ecto.Changeset
  require Logger

  schema "dealt_cards" do
    field :played_in_round, :integer

    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :card, Copi.Cornucopia.Card

    has_many :votes, Copi.Cornucopia.Vote

    timestamps()
  end

  def find(id) do
    case Ecto.Type.cast(:integer, id) do
      {:ok, cast_id} ->
        case Copi.Repo.get(Copi.Cornucopia.DealtCard, cast_id) do
          nil ->
            Logger.debug("Dealt card not found: #{inspect(id)}")
            {:error, :not_found}
          dealt_card -> {:ok, dealt_card  |> Copi.Repo.preload([:card, :votes])}
        end

      :error ->
        Logger.debug("DealtCard find called with invalid id format: #{inspect(id)}")
        {:error, :not_found}
    end
  end
  @doc false
  def changeset(dealt_card, attrs) do
    dealt_card
    |> cast(attrs, [])
    |> validate_required([])
  end
end
