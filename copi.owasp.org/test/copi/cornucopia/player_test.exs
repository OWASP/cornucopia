defmodule Copi.Cornucopia.PlayerTest do
  use ExUnit.Case, async: true

  alias Copi.Cornucopia.Player

  describe "changeset/2" do
    test "valid with name only" do
      # game_id is not in validate_required, so name alone is enough
      changeset = Player.changeset(%Player{}, %{name: "Alice"})
      assert changeset.valid?
    end

    test "invalid without name" do
      changeset = Player.changeset(%Player{}, %{})
      refute changeset.valid?
      assert %{name: ["can't be blank"]} = errors_on(changeset)
    end

    test "invalid when name too long" do
      changeset = Player.changeset(%Player{}, %{name: String.duplicate("a", 51)})
      refute changeset.valid?
    end
  end

  defp errors_on(changeset) do
    Ecto.Changeset.traverse_errors(changeset, fn {msg, opts} ->
      Enum.reduce(opts, msg, fn {key, value}, acc ->
        String.replace(acc, "%{#{key}}", to_string(value))
      end)
    end)
  end
end
