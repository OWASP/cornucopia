defmodule Copi.Cornucopia.Player do
  use Ecto.Schema
  import Ecto.Changeset
  require Logger

  @primary_key {:id, Ecto.ULID, autogenerate: true}
  @foreign_key_type Ecto.ULID

  schema "players" do
    field :name, Copi.Encrypted.Binary

    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID
    has_many :dealt_cards, Copi.Cornucopia.DealtCard

    timestamps()
  end

  def find(id) do
    case Ecto.ULID.cast(id) do
      {:ok, cast_id} ->
        case Copi.Repo.get(Copi.Cornucopia.Player, cast_id) do
          nil ->
            Logger.debug("Player not found: #{inspect(id)}")
            {:error, :not_found}
          player -> {:ok, player |> Copi.Repo.preload([:game, dealt_cards: [:card, :votes]])}
        end

      :error ->
        Logger.debug("Player find called with invalid id format: #{inspect(id)}")
        {:error, :not_found}
    end
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name, :game_id])
    |> validate_required([:name])
    |> validate_length(:name, min: 1, max: 50)
  end
end