defmodule Copi.ReleaseTest do
  use ExUnit.Case, async: false

  test "migrate runs with empty repo list" do
    old_repos = Application.get_env(:copi, :ecto_repos)

    try do
      Application.put_env(:copi, :ecto_repos, [])
      assert [] == Copi.Release.migrate()
    after
      Application.put_env(:copi, :ecto_repos, old_repos || [])
    end
  end

  test "rollback delegates to migrator for given repo" do
    assert_raise UndefinedFunctionError, fn ->
      Copi.Release.rollback(Copi.NoSuchRepo, 1)
    end
  end
end
