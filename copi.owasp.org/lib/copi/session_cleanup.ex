defmodule Copi.SessionCleanup do
  @moduledoc false

  use Task

  import Ecto.Query

  alias Copi.Repo
  alias Copi.SessionRecord

  def start_link(_opts) do
    Task.start_link(__MODULE__, :run, [])
  end

  def run do
    if Application.get_env(:copi, :postgres_session_store_enabled, false) do
      delete_expired_sessions(DateTime.utc_now())
    else
      :ok
    end
  end

  def delete_expired_sessions(now) do
    {deleted_count, _} =
      Repo.delete_all(from session in SessionRecord, where: session.expires_at <= ^now)

    {:ok, deleted_count}
  end
end
