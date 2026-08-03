defmodule Copi.Release do
  @moduledoc """
  Used for executing DB release tasks when run in production without Mix
  installed.
  """
  @app :copi
  @repo_stop_timeout 30_000

  def migrate do
    load_app()

    for repo <- repos() do
      {:ok, _, _} = with_repo(repo, &Ecto.Migrator.run(&1, :up, all: true))
    end
  end

  def rollback(repo, version) do
    load_app()
    {:ok, _, _} = with_repo(repo, &Ecto.Migrator.run(&1, :down, to: version))
  end

  defp repos do
    Application.fetch_env!(@app, :ecto_repos)
  end

  defp load_app do
    Application.load(@app)
  end

  defp with_repo(repo, operation) do
    config = repo.config()
    mode = :temporary

    {:ok, ecto_started} = Application.ensure_all_started(:ecto_sql, mode)
    {:ok, adapter_started} = repo.__adapter__().ensure_all_started(config, mode)
    started = ecto_started ++ adapter_started

    case repo.start_link(pool_size: 2) do
      {:ok, _pid} ->
        try do
          {:ok, operation.(repo), started}
        after
          repo.stop(@repo_stop_timeout)
        end

      {:error, {:already_started, _pid}} ->
        {:ok, operation.(repo), started}

      {:error, _reason} = error ->
        error
    end
  end
end
