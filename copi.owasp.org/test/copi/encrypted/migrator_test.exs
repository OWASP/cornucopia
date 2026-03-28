defmodule Copi.Encrypted.MigratorTest do
  use Copi.DataCase

  alias Copi.Encrypted.Migrator

  setup do
    key = :crypto.strong_rand_bytes(32) |> Base.encode64()
    System.put_env("COPI_ENCRYPTION_KEY", key)
    on_exit(fn -> System.delete_env("COPI_ENCRYPTION_KEY") end)
    :ok
  end

  test "run/0 returns {0, 0} when key is not set" do
    System.delete_env("COPI_ENCRYPTION_KEY")
    assert {0, 0} = Migrator.run()
  end

  test "run/0 returns {0, 0} when no rows exist" do
    assert {0, 0} = Migrator.run()
  end

  test "run/0 encrypts existing plaintext game names" do
    {:ok, _game} = Copi.Cornucopia.create_game(%{
      name: "Test Game",
      edition: "webapp"
    })
    assert {1, 0} = Migrator.run()
  end

  test "run/0 skips already encrypted rows on second run" do
    {:ok, _game} = Copi.Cornucopia.create_game(%{
      name: "Test Game",
      edition: "webapp"
    })
    Migrator.run()
    assert {0, 0} = Migrator.run()
  end
end