defmodule Copi.ReleaseTest do
  use ExUnit.Case, async: false
  import ExUnit.CaptureLog

  defmodule FailingAdapter do
    def ensure_all_started(_config, _mode), do: {:ok, []}
  end

  defmodule FailingRepo do
    def config, do: []
    def __adapter__, do: Copi.ReleaseTest.FailingAdapter
    def start_link(_opts), do: {:error, :boom}
  end

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

  test "migrate executes migrator loop for configured repo" do
    old_repos = Application.get_env(:copi, :ecto_repos)

    try do
      Application.put_env(:copi, :ecto_repos, [Copi.NoSuchRepo])

      assert_raise UndefinedFunctionError, fn ->
        Copi.Release.migrate()
      end
    after
      Application.put_env(:copi, :ecto_repos, old_repos || [])
    end
  end

  test "rollback with real repo without sandbox ownership fails in expected way" do
    capture_log(fn ->
      failure_mode =
        try do
          Copi.Release.rollback(Copi.Repo, 9_999_999_999)
          :unexpected_success
        rescue
          DBConnection.OwnershipError -> :ownership_error
        catch
          :exit, reason ->
            if inspect(reason) =~ "owner" and inspect(reason) =~ "exited" do
              :owner_exited
            else
              reraise "Unexpected exit reason: #{inspect(reason)}", __STACKTRACE__
            end
        end

      assert failure_mode in [:ownership_error, :owner_exited]
    end)
  end

  test "migrate surfaces repo start errors that are not already_started" do
    old_repos = Application.get_env(:copi, :ecto_repos)

    try do
      Application.put_env(:copi, :ecto_repos, [FailingRepo])

      assert_raise MatchError, fn ->
        Copi.Release.migrate()
      end
    after
      Application.put_env(:copi, :ecto_repos, old_repos || [])
    end
  end
end
