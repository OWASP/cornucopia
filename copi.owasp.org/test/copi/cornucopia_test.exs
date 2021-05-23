defmodule Copi.CornucopiaTest do
  use Copi.DataCase

  alias Copi.Cornucopia

  describe "games" do
    alias Copi.Cornucopia.Game

    @valid_attrs %{created_at: "2010-04-17T14:00:00Z", finished_at: "2010-04-17T14:00:00Z", name: "some name", started_at: "2010-04-17T14:00:00Z"}
    @update_attrs %{created_at: "2011-05-18T15:01:01Z", finished_at: "2011-05-18T15:01:01Z", name: "some updated name", started_at: "2011-05-18T15:01:01Z"}
    @invalid_attrs %{created_at: nil, finished_at: nil, name: nil, started_at: nil}

    def game_fixture(attrs \\ %{}) do
      {:ok, game} =
        attrs
        |> Enum.into(@valid_attrs)
        |> Cornucopia.create_game()

      game
    end

    test "list_games/0 returns all games" do
      game = game_fixture()
      assert Cornucopia.list_games() == [game]
    end

    test "get_game!/1 returns the game with given id" do
      game = game_fixture()
      assert Cornucopia.get_game!(game.id) == game
    end

    test "create_game/1 with valid data creates a game" do
      assert {:ok, %Game{} = game} = Cornucopia.create_game(@valid_attrs)
      assert game.created_at == DateTime.from_naive!(~N[2010-04-17T14:00:00Z], "Etc/UTC")
      assert game.finished_at == DateTime.from_naive!(~N[2010-04-17T14:00:00Z], "Etc/UTC")
      assert game.name == "some name"
      assert game.started_at == DateTime.from_naive!(~N[2010-04-17T14:00:00Z], "Etc/UTC")
    end

    test "create_game/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Cornucopia.create_game(@invalid_attrs)
    end

    test "update_game/2 with valid data updates the game" do
      game = game_fixture()
      assert {:ok, %Game{} = game} = Cornucopia.update_game(game, @update_attrs)
      assert game.created_at == DateTime.from_naive!(~N[2011-05-18T15:01:01Z], "Etc/UTC")
      assert game.finished_at == DateTime.from_naive!(~N[2011-05-18T15:01:01Z], "Etc/UTC")
      assert game.name == "some updated name"
      assert game.started_at == DateTime.from_naive!(~N[2011-05-18T15:01:01Z], "Etc/UTC")
    end

    test "update_game/2 with invalid data returns error changeset" do
      game = game_fixture()
      assert {:error, %Ecto.Changeset{}} = Cornucopia.update_game(game, @invalid_attrs)
      assert game == Cornucopia.get_game!(game.id)
    end

    test "delete_game/1 deletes the game" do
      game = game_fixture()
      assert {:ok, %Game{}} = Cornucopia.delete_game(game)
      assert_raise Ecto.NoResultsError, fn -> Cornucopia.get_game!(game.id) end
    end

    test "change_game/1 returns a game changeset" do
      game = game_fixture()
      assert %Ecto.Changeset{} = Cornucopia.change_game(game)
    end
  end

  describe "players" do
    alias Copi.Cornucopia.Player

    @valid_attrs %{name: "some name"}
    @update_attrs %{name: "some updated name"}
    @invalid_attrs %{name: nil}

    def player_fixture(attrs \\ %{}) do
      {:ok, player} =
        attrs
        |> Enum.into(@valid_attrs)
        |> Cornucopia.create_player()

      player
    end

    test "list_players/0 returns all players" do
      player = player_fixture()
      assert Cornucopia.list_players() == [player]
    end

    test "get_player!/1 returns the player with given id" do
      player = player_fixture()
      assert Cornucopia.get_player!(player.id) == player
    end

    test "create_player/1 with valid data creates a player" do
      assert {:ok, %Player{} = player} = Cornucopia.create_player(@valid_attrs)
      assert player.name == "some name"
    end

    test "create_player/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Cornucopia.create_player(@invalid_attrs)
    end

    test "update_player/2 with valid data updates the player" do
      player = player_fixture()
      assert {:ok, %Player{} = player} = Cornucopia.update_player(player, @update_attrs)
      assert player.name == "some updated name"
    end

    test "update_player/2 with invalid data returns error changeset" do
      player = player_fixture()
      assert {:error, %Ecto.Changeset{}} = Cornucopia.update_player(player, @invalid_attrs)
      assert player == Cornucopia.get_player!(player.id)
    end

    test "delete_player/1 deletes the player" do
      player = player_fixture()
      assert {:ok, %Player{}} = Cornucopia.delete_player(player)
      assert_raise Ecto.NoResultsError, fn -> Cornucopia.get_player!(player.id) end
    end

    test "change_player/1 returns a player changeset" do
      player = player_fixture()
      assert %Ecto.Changeset{} = Cornucopia.change_player(player)
    end
  end
end
