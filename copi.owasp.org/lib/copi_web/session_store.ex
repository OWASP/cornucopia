defmodule CopiWeb.SessionStore do
  @moduledoc false

  @behaviour Plug.Session.Store

  import Ecto.Query

  alias Copi.Encrypted.Binary, as: EncryptedBinary
  alias Copi.Repo
  alias Copi.SessionRecord

  @postgres_session_id "postgres_session_id"

  @impl true
  def init(opts) do
    %{cookie: Plug.Session.COOKIE.init(opts)}
  end

  @impl true
  def get(conn, raw_cookie, %{cookie: cookie_opts}) do
    if postgres_enabled?() do
      get_from_postgres(conn, raw_cookie, cookie_opts)
    else
      Plug.Session.COOKIE.get(conn, raw_cookie, cookie_opts)
    end
  end

  @impl true
  def put(conn, session_id, session, %{cookie: cookie_opts}) do
    if postgres_enabled?() do
      put_in_postgres(conn, session_id, session, cookie_opts)
    else
      Plug.Session.COOKIE.put(conn, session_id, session, cookie_opts)
    end
  end

  @impl true
def delete(conn, session_id, %{cookie: cookie_opts}) do
  if postgres_enabled?() do
    Repo.delete_all(from record in SessionRecord, where: record.id == ^session_id)
    Plug.Session.COOKIE.delete(conn, session_id, cookie_opts)
  else
    Plug.Session.COOKIE.delete(conn, session_id, cookie_opts)
  end
end

  defp get_from_postgres(conn, raw_cookie, cookie_opts) do
    with {_cookie_id, %{@postgres_session_id => session_id}} when is_binary(session_id) <-
           Plug.Session.COOKIE.get(conn, raw_cookie, cookie_opts),
         %SessionRecord{} = record <- Repo.get(SessionRecord, session_id),
         :gt <- DateTime.compare(record.expires_at, DateTime.utc_now()),
         {:ok, session} when is_map(session) <- decrypt_database_session(record.data) do
      {session_id, session}
    else
      _ -> {nil, %{}}
    end
  end

  defp put_in_postgres(conn, session_id, session, cookie_opts) do
    session_id = session_id || new_session_id()
    now = DateTime.utc_now()
    expires_at = DateTime.add(now, session_ttl_seconds(), :second)
    {:ok, data} = encrypt_database_session(session)

    Repo.insert!(
      %SessionRecord{id: session_id, data: data, expires_at: expires_at},
      on_conflict: [set: [data: data, expires_at: expires_at]],
      conflict_target: [:id]
    )

    Repo.delete_all(from record in SessionRecord, where: record.expires_at <= ^now)

    Plug.Session.COOKIE.put(
      conn,
      nil,
      %{@postgres_session_id => session_id},
      cookie_opts
    )
  end

  defp encrypt_database_session(session) do
    session
    |> :erlang.term_to_binary(compressed: 6)
    |> EncryptedBinary.encrypt()
  end

  defp decrypt_database_session(data) do
    with {:ok, plaintext} <- EncryptedBinary.decrypt(data) do
      {:ok, Plug.Crypto.non_executable_binary_to_term(plaintext)}
    end
  rescue
    ArgumentError -> {:error, :invalid_session}
  end

  defp new_session_id do
    32
    |> :crypto.strong_rand_bytes()
    |> Base.url_encode64(padding: false)
  end

  defp postgres_enabled? do
    Application.get_env(:copi, :postgres_session_store_enabled, false)
  end

  defp session_ttl_seconds do
    Application.fetch_env!(:copi, :session_ttl_seconds)
  end
end
