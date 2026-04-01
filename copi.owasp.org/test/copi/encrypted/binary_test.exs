defmodule Copi.Encrypted.BinaryTest do
  use ExUnit.Case, async: true
  alias Copi.Encrypted.Binary, as: EncryptedBinary

  setup do
    key = :crypto.strong_rand_bytes(32) |> Base.encode64()
    System.put_env("COPI_ENCRYPTION_KEY", key)
    on_exit(fn -> System.delete_env("COPI_ENCRYPTION_KEY") end)
    :ok
  end

  test "type is :binary" do
    assert EncryptedBinary.type() == :binary
  end

  test "cast accepts a string" do
    assert {:ok, "hello"} = EncryptedBinary.cast("hello")
  end

  test "cast rejects non-strings" do
    assert :error = EncryptedBinary.cast(42)
    assert :error = EncryptedBinary.cast(nil)
  end

  test "dump nil returns nil" do
    assert {:ok, nil} = EncryptedBinary.dump(nil)
  end

  test "dump produces blob with ENC1 prefix" do
    {:ok, blob} = EncryptedBinary.dump("test game")
    assert binary_part(blob, 0, 4) == "ENC1"
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

  test "legacy plaintext passes through load" do
    assert {:ok, "old name"} = EncryptedBinary.load("old name")
  end

  test "tampered blob raises on load" do
    {:ok, blob} = EncryptedBinary.dump("secret")
    <<header::binary-32, byte, rest::binary>> = blob
    tampered = header <> <<Bitwise.bxor(byte, 0xFF)>> <> rest
    assert_raise RuntimeError, fn ->
      EncryptedBinary.load(tampered)
    end
  end

  test "wrong key raises on load" do
    {:ok, blob} = EncryptedBinary.dump("secret")
    System.put_env("COPI_ENCRYPTION_KEY", Base.encode64(:crypto.strong_rand_bytes(32)))
    assert_raise RuntimeError, fn ->
      EncryptedBinary.load(blob)
    end
  end

  test "missing key raises on dump" do
    System.delete_env("COPI_ENCRYPTION_KEY")
    Application.delete_env(:copi, :encryption_key)
    assert_raise RuntimeError, fn ->
      EncryptedBinary.dump("anything")
    end
  after
    Application.put_env(:copi, :encryption_key, "MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTI=")
  end
end