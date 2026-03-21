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
    sanitized = sanitize_name(name)
    
    # Check if the sanitized version is different from original (indicating dangerous content was removed)
    sanitized != name or
    # Or check if the sanitized version contains only safe characters
    String.match?(sanitized, ~r/^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\uFDF2\uFDF3\uFDF4\uFDFD\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9F\u3400-\u4DBF\uF900-\uFAFF\u0900-\u097F\u0621-\u064A\u0660-\u0669\u0E00-\u0E7F\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u0370-\u03FF\u1F00-\u1FFFA-Za-zÀ-ÖØ-öø-ÿĀ-ž0-9._\--ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي\s]+$/u)
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
    |> String.replace("\"", "&quot;")
    |> String.replace("'", "&#39;")
  end
end
