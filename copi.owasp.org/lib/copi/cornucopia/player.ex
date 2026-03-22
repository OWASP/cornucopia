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
    String.match?(
      name,
      ~r/^[
        \x{0600}-\x{06FF}          
        \x{0750}-\x{077F}          
        \x{08A0}-\x{08FF}          
        \x{FB50}-\x{FDFF}          
        \x{FE70}-\x{FEFF}          
        \x{FDF2}\x{FDF3}\x{FDF4}\x{FDFD}
        \x{3040}-\x{309F}          
        \x{30A0}-\x{30FF}          
        \x{4E00}-\x{9FFF}          
        \x{FF66}-\x{FF9F}          
        ー々〆〤                   
        \x{3400}-\x{4DBF}          
        \x{F900}-\x{FAFF}           
        \x{0900}-\x{097F}          
        \x{0621}-\x{064A}          
        \x{0660}-\x{0669}          
        \x{0E00}-\x{0E7F}          
        «»฿ฯ๏๚๛                    
        \x{0400}-\x{04FF}          
        \x{0500}-\x{052F}          
        \x{2DE0}-\x{2DFF}          
        \x{A640}-\x{A69F}          
        Ю́ю́Я́я́                       
        \x{0370}-\x{03FF}          
        \x{1F00}-\x{1FFF}          
        A-Za-z                     
        À-ÖØ-öø-ÿĀ-ž              
        0-9                       
        ._\-'"                    
        ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي 
        ًٌٍَُِّْٰﷲﷴﷺﷻ                    
        ٠١٢٣٤٥٦٧٨٩             
        \s                          
      ]+$/ux
    )
  end

  defp valid_name?(_), do: false
end
