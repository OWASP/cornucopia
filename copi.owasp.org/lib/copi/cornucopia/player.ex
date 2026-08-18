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
        |> validate_format(:name, ~r/^[\x{0600}-\x{06FF}\x{0750}-\x{077F}\x{08A0}-\x{08FF}\x{FB50}-\x{FDFF}\x{FE70}-\x{FEFF}\x{FDF2}\x{FDF3}\x{FDF4}\x{FDFD}\x{3040}-\x{309F}\x{30A0}-\x{30FF}\x{4E00}-\x{9FFF}\x{FF66}-\x{FF9F}\x{3400}-\x{4DBF}\x{F900}-\x{FAFF}\x{0900}-\x{097F}\x{0621}-\x{064A}\x{0660}-\x{0669}\x{0E00}-\x{0E7F}\x{0400}-\x{04FF}\x{0500}-\x{052F}\x{2DE0}-\x{2DFF}\x{A640}-\x{A69F}\x{0370}-\x{03FF}\x{1F00}-\x{1FFF}A-Za-z\x{00C0}-\x{00D6}\x{00D8}-\x{00F6}\x{00F8}-\x{00FF}\x{0100}-\x{017E}0-9._\- ]+$/u, message: "contains invalid characters. Only letters, numbers, spaces, and ._- are allowed.")
  end
end
