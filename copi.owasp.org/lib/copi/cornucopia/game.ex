 defmodule Copi.Cornucopia.Game do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, Ecto.ULID, autogenerate: true}

  schema "games" do
    field :created_at, :utc_datetime, default: DateTime.truncate(DateTime.utc_now(), :second)
    field :finished_at, :utc_datetime
    field :name, :string
    field :edition, :string
    field :started_at, :utc_datetime
    field :rounds_played, :integer, default: 0
    field :suits, {:array, :string}, default: []
    field :round_open, :boolean, default: true

    has_many :players, Copi.Cornucopia.Player
    has_many :continue_votes, Copi.Cornucopia.ContinueVote

    timestamps()
  end

  def find(id) do
    case Copi.Repo.get(Copi.Cornucopia.Game, id) do
      nil -> {:error, :not_found}
      game -> {:ok, game |> Copi.Repo.preload([players: [dealt_cards: [:card, :votes]], continue_votes: [:player]])}
    end
  end

  @doc false
  def changeset(game, attrs) do
    game
    |> cast(attrs, [:name, :created_at, :edition, :started_at, :finished_at, :rounds_played, :suits, :round_open])
    |> validate_required([:name], message: "No really, give your game session a name")
    |> validate_length(:name, min: 1, max: 100)
    |> validate_name(:name)
  end

  def continue_vote_count(game) do
    Enum.count(game.continue_votes)
  end

  def has_continue_vote?(game, player) do
    Enum.any?(game.continue_votes, fn vote -> vote.player_id == player.id end)
  end

  def majority_continue_votes_reached?(game) do
    total_players = Enum.count(game.players)
    continue_votes = continue_vote_count(game)
    
    continue_votes > div(total_players, 2)
  end

  def can_continue_round?(game) do
    round_open?(game) and majority_continue_votes_reached?(game)
  end

  def round_open?(game) do
    latest_round = game.rounds_played + 1

    players_still_to_play = game.players |> Enum.filter(fn player -> 
      Enum.find(player.dealt_cards, fn card -> card.played_in_round == latest_round end) == nil 
    end)

    Enum.count(players_still_to_play) > 0
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
