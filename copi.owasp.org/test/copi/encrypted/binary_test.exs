defmodule Copi.Encrypted.BinaryTest do
  use ExUnit.Case, async: true

  alias Copi.Encrypted.Binary, as: EncryptedBinary

  test "type is :binary" do
    assert EncryptedBinary.type() == :binary
  end

  test "cast accepts a string" do
    assert {:ok, "hello"} = EncryptedBinary.cast("hello")
  end

  test "cast accepts nil" do
    assert {:ok, nil} = EncryptedBinary.cast(nil)
  end

  test "cast rejects non-strings" do
    assert :error = EncryptedBinary.cast(42)
  end

  test "dump nil returns nil" do
    assert {:ok, nil} = EncryptedBinary.dump(nil)
  end

  test "dump produces encrypted binary" do
    {:ok, blob} = EncryptedBinary.dump("test game")
    assert is_binary(blob)
    assert byte_size(blob) > 0
  end

  test "same input gives different blobs each time" do
    {:ok, b1} = EncryptedBinary.dump("same")
    {:ok, b2} = EncryptedBinary.dump("same")
    refute b1 == b2
  end

  test "load nil returns nil" do
    assert {:ok, nil} = EncryptedBinary.load(nil)
  end

  test "round trip game name" do
    {:ok, blob} = EncryptedBinary.dump("My Game")
    assert {:ok, "My Game"} = EncryptedBinary.load(blob)
  end

  test "round trip player name" do
    {:ok, blob} = EncryptedBinary.dump("Alice")
    assert {:ok, "Alice"} = EncryptedBinary.load(blob)
  end
end