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
    |> validate_format(:name, ~r/^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\uFDF2\uFDF3\uFDF4\uFDFD\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9Fー々〆〤\u3400-\u4DBF\uF900-\uFAFF\u0900-\u097F\u0621-\u064A\u0660-\u0669\u0E00-\u0E7F«»฿ฯ๏๚๛\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69FЮ́ю́Я́я́\u0370-\u03FF\u1F00-\u1FFFA-Za-zÀ-ÖØ-öø-ÿĀ-ž0-9._\--ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي ًٌٍَُِّْٰﷲﷴﷺﷻ ٠١٢٣٤٥٦٧٨٩ \s]+$/,
      message: "contains invalid characters. Only letters, numbers, spaces, and ._- are allowed.")
  end
end