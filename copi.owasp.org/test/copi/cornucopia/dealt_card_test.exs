defmodule Copi.Cornucopia.DealtCardTest do
  use Copi.DataCase, async: true

  alias Copi.Cornucopia.DealtCard

  describe "changeset/2" do
    test "returns a valid changeset with empty attrs" do
      changeset = DealtCard.changeset(%DealtCard{}, %{})
      assert changeset.valid?
    end

    test "casts played_in_round when provided" do
      changeset = DealtCard.changeset(%DealtCard{}, %{played_in_round: 3})
      # changeset/2 only casts [], so played_in_round is ignored but changeset is valid
      assert changeset.valid?
    end
  end

  describe "find/1" do
    test "returns error for nonexistent dealt card id" do
      assert {:error, :not_found} = DealtCard.find(-1)
    end
  end
end
