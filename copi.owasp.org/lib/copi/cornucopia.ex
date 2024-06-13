defmodule Copi.Cornucopia do
  @moduledoc """
  The Cornucopia context.
  """

  import Ecto.Query, warn: false
  alias Copi.Repo

  alias Copi.Cornucopia.Game

  @doc """
  Returns the list of games.

  ## Examples

      iex> list_games()
      [%Game{}, ...]

  """
  def list_games do
    Repo.all(Game)
  end

  @doc """
  Gets a single game.

  Raises `Ecto.NoResultsError` if the Game does not exist.

  ## Examples

      iex> get_game!(123)
      %Game{}

      iex> get_game!(456)
      ** (Ecto.NoResultsError)

  """
  def get_game!(id), do: Repo.get!(Game, id)

  @doc """
  Creates a game.

  ## Examples

      iex> create_game(%{field: value})
      {:ok, %Game{}}

      iex> create_game(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_game(attrs \\ %{}) do
    %Game{}
    |> Game.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a game.

  ## Examples

      iex> update_game(game, %{field: new_value})
      {:ok, %Game{}}

      iex> update_game(game, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_game(%Game{} = game, attrs) do
    game
    |> Game.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a game.

  ## Examples

      iex> delete_game(game)
      {:ok, %Game{}}

      iex> delete_game(game)
      {:error, %Ecto.Changeset{}}

  """
  def delete_game(%Game{} = game) do
    Repo.delete(game)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking game changes.

  ## Examples

      iex> change_game(game)
      %Ecto.Changeset{data: %Game{}}

  """
  def change_game(%Game{} = game, attrs \\ %{}) do
    Game.changeset(game, attrs)
  end

  alias Copi.Cornucopia.Player

  @doc """
  Returns the list of players.

  ## Examples

      iex> list_players()
      [%Player{}, ...]

  """

  def list_players(game_id) do

    Repo.all(from p in Player, where: p.game_id == ^game_id)
  end

  @doc """
  Gets a single player.

  Raises `Ecto.NoResultsError` if the Player does not exist.

  ## Examples

      iex> get_player!(123)
      %Player{}

      iex> get_player!(456)
      ** (Ecto.NoResultsError)

  """
  def get_player!(id), do: Repo.get!(Player, id)

  @doc """
  Creates a player.

  ## Examples

      iex> create_player(%{field: value})
      {:ok, %Player{}}

      iex> create_player(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_player(attrs \\ %{}) do
    %Player{}
    |> Player.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a player.

  ## Examples

      iex> update_player(player, %{field: new_value})
      {:ok, %Player{}}

      iex> update_player(player, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_player(%Player{} = player, attrs) do
    player
    |> Player.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a player.

  ## Examples

      iex> delete_player(player)
      {:ok, %Player{}}

      iex> delete_player(player)
      {:error, %Ecto.Changeset{}}

  """
  def delete_player(%Player{} = player) do
    Repo.delete(player)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking player changes.

  ## Examples

      iex> change_player(player)
      %Ecto.Changeset{data: %Player{}}

  """
  def change_player(%Player{} = player, attrs \\ %{}) do
    Player.changeset(player, attrs)
  end

  alias Copi.Cornucopia.Card

  @doc """
  Returns the list of cards.

  ## Examples

      iex> list_cards()
      [%Card{}, ...]

  """
  def list_cards do
    Card |> order_by(:id) |> Repo.all()
  end

  def list_cards_shuffled(edition) do
    Card |> where(edition: ^edition) |> order_by(fragment("RANDOM()")) |> Repo.all()
  end

  @doc """
  Gets a single card.

  Raises `Ecto.NoResultsError` if the Card does not exist.

  ## Examples

      iex> get_card!(123)
      %Card{}

      iex> get_card!(456)
      ** (Ecto.NoResultsError)

  """
  def get_card!(id), do: Repo.get!(Card, id)

  @doc """
  Gets a single card from its external id.

  Raises `Ecto.NoResultsError` if the Card does not exist.

  ## Examples

      iex> get_card_by_external_id!(DV2)
      %Card{}

      iex>get_card_by_external_id!(XXX)
      ** (Ecto.NoResultsError)

  """
  def get_card_by_external_id!(version, external_id), do: Repo.get_by!(Card, [version: version, external_id: external_id])

  @doc """
  Creates a card.

  ## Examples

      iex> create_card(%{field: value})
      {:ok, %Card{}}

      iex> create_card(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_card(attrs \\ %{}) do
    %Card{}
    |> Card.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a card.

  ## Examples

      iex> update_card(card, %{field: new_value})
      {:ok, %Card{}}

      iex> update_card(card, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_card(%Card{} = card, attrs) do
    card
    |> Card.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a card.

  ## Examples

      iex> delete_card(card)
      {:ok, %Card{}}

      iex> delete_card(card)
      {:error, %Ecto.Changeset{}}

  """
  def delete_card(%Card{} = card) do
    Repo.delete(card)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking card changes.

  ## Examples

      iex> change_card(card)
      %Ecto.Changeset{data: %Card{}}

  """
  def change_card(%Card{} = card, attrs \\ %{}) do
    Card.changeset(card, attrs)
  end

  def highest_scoring_cards_in_game(game) do
    Enum.reduce(game.players, [], fn player, cards -> (player.dealt_cards |> played_cards) ++ cards end) # Combine all played cards from all players
      |> lead_suit_cards # Filter to just the lead suit cards
      |> scoring_cards(Enum.count(game.players)) # Filter to just the cards that scored
      |> Enum.group_by(fn card -> card.played_in_round end) # Convert to map where {round, [scoring_cards]}
      |> Enum.flat_map(fn {_, cards} -> highest_card(cards) end) # Back to a list of just the highest scoring card in each round
  end

  def highest_scoring_cards_for_player(player, game) do
    highest_scoring_cards_in_game(game)
      |> Enum.filter(fn dealt_card -> dealt_card.player_id == player.id end)
  end

  def highest_scoring_card_in_round(game, round) do
    highest_scoring_cards_in_game(game)
      |> Enum.find(fn dealt_card -> dealt_card.played_in_round == round end)
  end

  defp highest_card(cards) do
    card_order = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "JokerB", "JokerA"]

    Enum.group_by(cards, fn dealt_card -> Enum.find_index(card_order, fn value -> value == dealt_card.card.value end) end)
      |> Enum.max_by(fn {index, _cards} -> index end)
      |> elem(1)
  end

  def unplayed_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round == nil end)
  end

  def played_cards(cards) do
    Enum.filter(cards, fn card -> card.played_in_round != nil end)
  end

  def scoring_cards(cards, number_of_players) do
    Enum.filter(cards, fn card -> card.played_in_round != nil && Enum.count(card.votes) > (number_of_players - 1) / 2 end)
  end

  def lead_suit_cards(cards) do
    Enum.group_by(cards, fn card -> card.played_in_round end) # Convert to map where {round, [played_cards]}
      |> Map.new(fn {round, played_cards} -> {round, Enum.sort_by(played_cards, &(&1.updated_at))} end) # Sort played cards in rounds by when played
      |> Enum.flat_map(fn {_round, ordered_played_cards} -> Enum.filter(ordered_played_cards, fn card -> card.card.category == List.first(ordered_played_cards).card.category or card.card.value in ["JokerA", "JokerB"] or String.upcase(card.card.category) == "CORNUCOPIA" end) end) # Back to a list of just the lead suit cards in each round (plus jokers and trump cards)
  end
end
