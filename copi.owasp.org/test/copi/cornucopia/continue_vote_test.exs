defmodule Copi.Cornucopia.ContinueVoteTest do
  use Copi.DataCase

  alias Copi.Cornucopia.ContinueVote

  describe "continue_votes" do
    @valid_attrs %{player_id: Ecto.ULID.generate(), game_id: Ecto.ULID.generate()}
    @invalid_attrs %{player_id: nil, game_id: nil}

    test "changeset with valid attributes" do
      changeset = ContinueVote.changeset(%ContinueVote{}, @valid_attrs)
      assert changeset.valid?
    end

    test "changeset with invalid attributes" do
      changeset = ContinueVote.changeset(%ContinueVote{}, @invalid_attrs)
      refute changeset.valid?
      assert "can't be blank" in errors_on(changeset).player_id
      assert "can't be blank" in errors_on(changeset).game_id
    end
  end
end
