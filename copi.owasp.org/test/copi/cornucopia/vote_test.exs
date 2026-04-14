defmodule Copi.Cornucopia.VoteTest do
  use Copi.DataCase

  alias Copi.Cornucopia.Vote

  describe "votes" do
    @valid_attrs %{dealt_card_id: 1, player_id: Ecto.ULID.generate()}
    @invalid_attrs %{dealt_card_id: nil, player_id: nil}

    test "changeset with valid attributes" do
      changeset = Vote.changeset(%Vote{}, @valid_attrs)
      assert changeset.valid?
    end

    test "changeset with invalid attributes" do
      changeset = Vote.changeset(%Vote{}, @invalid_attrs)
      refute changeset.valid?
      assert "can't be blank" in errors_on(changeset).dealt_card_id
      assert "can't be blank" in errors_on(changeset).player_id
    end
  end
end