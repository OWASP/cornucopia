defmodule Copi.Cornucopia.Player do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}
  @foreign_key_type Ecto.ULID

  schema "players" do
    field :name, Copi.Encrypted.Binary

    belongs_to :game, Copi.Cornucopia.Game, type: Ecto.ULID
    has_many :dealt_cards, Copi.Cornucopia.DealtCard

    timestamps()
  end

  def find(id) do
    case Copi.Repo.get(Copi.Cornucopia.Player, id) do
      nil -> {:error, :not_found}
      player -> {:ok, player |> Copi.Repo.preload([:game, dealt_cards: [:card, :votes]])}
    end
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name, :game_id])
    |> validate_required([:name])
    |> validate_length(:name, min: 1, max: 50)
    |> validate_format(:name, ~r/^[\x{0600}-\x{06FF}\x{0750}-\x{077F}\x{08A0}-\x{08FF}\x{FB50}-\x{FDFF}\x{FE70}-\x{FEFF}\x{FDF2}\x{FDF3}\x{FDF4}\x{FDFD}\x{3040}-\x{309F}\x{30A0}-\x{30FF}\x{4E00}-\x{9FFF}\x{FF66}-\x{FF9F}ー々〆〤\x{3400}-\x{4DBF}\x{F900}-\x{FAFF}\x{0900}-\x{097F}\x{0621}-\x{064A}\x{0660}-\x{0669}\x{0E00}-\x{0E7F}«»฿ฯ๏๚๛\x{0400}-\x{04FF}\x{0500}-\x{052F}\x{2DE0}-\x{2DFF}\x{A640}-\x{A69F}Ю́ю́Я́я́\x{0370}-\x{03FF}\x{1F00}-\x{1FFFA-Za-zÀ-ÖØ-öø-ÿĀ-ž0-9._\--ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي ًٌٍَُِّْٰﷲﷴﷺﷻ ٠١٢٣٤٥٦٧٨٩ \s]+$/,
      message: "contains invalid characters. Only letters, numbers, spaces, and ._- are allowed.")
  end
end