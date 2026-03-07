defmodule Copi.Cornucopia.VoteTest do
  use ExUnit.Case, async: true

  alias Copi.Cornucopia.Vote

  describe "changeset/2" do
    test "valid with empty attrs" do
      changeset = Vote.changeset(%Vote{}, %{})
      assert changeset.valid?
    end
  end
end
