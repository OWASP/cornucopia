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
      player -> {:ok, player |> Copi.Repo.preload([:game, dealt_cards: [:card, :votes]])}
    end
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name, :game_id])
    |> validate_required([:name])
    |> validate_length(:name, min: 1, max: 50)
    |> validate_name(:name)
  end

  # Input validation and sanitization to prevent XSS
  defp validate_name(changeset, field) do
    case Ecto.Changeset.get_field(changeset, field) do
      nil -> changeset
      name when is_binary(name) ->
        if valid_name?(name) do
          changeset
        else
          Ecto.Changeset.add_error(
            changeset, 
            field, 
            "contains unsafe content. Please use only letters, numbers, spaces, and basic punctuation."
          )
        end
      _ ->
        changeset
    end
  end

  defp valid_name?(name) when is_binary(name) and name != "" do
    sanitized = sanitize_name(name)
    
    # Check if the sanitized version is different from original (indicating dangerous content was removed)
    sanitized != name or
    # Or check if the sanitized version contains only safe characters
    String.match?(sanitized, ~r/^[\u0600-\u06FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\uFDF2\uFDF3\uFDF4\uFDFD\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9Fー々〆〤\u3400-\u4DBF\uF900-\uFAFF\u0900-\u097F\u0621-\u064A\u0660-\u0669\u4E00-\u9FFF\u0E00-\u0E7F«»฿ฯ๏๚๛\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69FЮ́ю́Я́я́\u0370-\u03FF\u1F00-\u1FFFA-Za-zÀ-ÖØ-öø-ÿĀ-ž0-9._\--ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي ًٌٍَُِّْٰﷲﷴﷺﷻ ٠١٢٣٤٥٦٧٨٩ \s]+$/u)
  end

  defp valid_name?(_), do: false

  defp sanitize_name(name) when is_binary(name) do
    name
    |> strip_html_tags()
    |> strip_javascript()
    |> strip_data_attributes()
    |> escape_html_entities()
    |> String.trim()
    |> String.replace(~r/\s+/, " ") # Normalize multiple spaces
  end

  defp sanitize_name(_), do: ""

  defp strip_html_tags(text) do
    # Remove HTML tags using regex
    String.replace(text, ~r/<[^>]*>/, "")
  end

  defp strip_javascript(text) do
    # Remove JavaScript patterns
    text
    |> String.replace(~r/javascript:/i, "")
    |> String.replace(~r/on\w+\s*=/i, "")
    |> String.replace(~r/eval\s*\(/i, "")
    |> String.replace(~r/Function\s*\(/i, "")
  end

  defp strip_data_attributes(text) do
    # Remove data-* attributes that could be used for XSS
    String.replace(text, ~r/data-\w+/, "")
  end

  defp escape_html_entities(text) do
    # Escape HTML entities that could be dangerous
    text
    |> String.replace("&", "&")
    |> String.replace("<", "<")
    |> String.replace(">", ">")
    |> String.replace("\"", """)
    |> String.replace("'", "&#39;")
  end
end
