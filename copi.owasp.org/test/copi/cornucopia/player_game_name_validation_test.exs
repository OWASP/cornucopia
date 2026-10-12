defmodule Copi.Cornucopia.NameValidationTest do
  use Copi.DataCase

  alias Copi.Cornucopia.Player
  alias Copi.Cornucopia.Game

  describe "player name validation" do
    test "accepts Latin characters" do
      changeset = Player.changeset(%Player{}, %{name: "Alice"})
      assert changeset.valid?
    end

    test "accepts Arabic characters" do
      changeset = Player.changeset(%Player{}, %{name: "محمد"})
      assert changeset.valid?
    end

    test "accepts Japanese characters" do
      changeset = Player.changeset(%Player{}, %{name: "田中"})
      assert changeset.valid?
    end

    test "accepts Cyrillic characters" do
      changeset = Player.changeset(%Player{}, %{name: "Иван"})
      assert changeset.valid?
    end

    test "accepts Greek characters" do
      changeset = Player.changeset(%Player{}, %{name: "Νίκος"})
      assert changeset.valid?
    end

    test "accepts Thai characters" do
      changeset = Player.changeset(%Player{}, %{name: "สมชาย"})
      assert changeset.valid?
    end

    test "rejects HTML tags" do
      changeset = Player.changeset(%Player{}, %{name: "<script>alert('XSS')</script>"})
      refute changeset.valid?
    end

    test "rejects JavaScript injection" do
      changeset = Player.changeset(%Player{}, %{name: "javascript:alert(1)"})
      refute changeset.valid?
    end
  end

  describe "game name validation" do
    test "accepts Latin characters" do
      changeset = Game.changeset(%Game{}, %{name: "My Game"})
      assert changeset.valid?
    end

    test "accepts Arabic characters" do
      changeset = Game.changeset(%Game{}, %{name: "لعبة"})
      assert changeset.valid?
    end

    test "rejects HTML tags" do
      changeset = Game.changeset(%Game{}, %{name: "<b>bold</b>"})
      refute changeset.valid?
    end

    test "rejects JavaScript injection" do
      changeset = Game.changeset(%Game{}, %{name: "<img src=x onerror=alert(1)>"})
      refute changeset.valid?
    end
  end
end