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
end
