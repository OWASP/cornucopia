defmodule CopiWeb.SessionStoreTest do
  use CopiWeb.ConnCase, async: false

  alias Copi.Encrypted.Binary, as: EncryptedBinary
  alias Copi.Repo
  alias Copi.SessionRecord
  alias CopiWeb.SessionStore

  setup do
    previous_postgres_enabled = Application.get_env(:copi, :postgres_session_store_enabled)
    previous_session_ttl = Application.get_env(:copi, :session_ttl_seconds)

    on_exit(fn ->
      restore_env(:postgres_session_store_enabled, previous_postgres_enabled)
      restore_env(:session_ttl_seconds, previous_session_ttl)
    end)

    opts =
      SessionStore.init(
        key: "_copi_key",
        signing_salt: "K7VwkdRe",
        encryption_salt: "vJ7hQp2L",
        secret_key_base: String.duplicate("a", 64)
      )

    %{opts: opts}
  end

  test "cookie mode stores, reads, and deletes sessions", %{conn: conn, opts: opts} do
    Application.put_env(:copi, :postgres_session_store_enabled, false)

    session = %{
      "resume_player_session" => [
        %{"game_id" => "game-1", "player_id" => "player-1"}
      ]
    }

    raw_cookie = SessionStore.put(conn, nil, session, opts)

    assert {session_id, ^session} = SessionStore.get(conn, raw_cookie, opts)
    assert is_binary(session_id)
    assert SessionStore.delete(conn, session_id, opts) == nil
  end

  test "postgres mode stores, restores, updates, and prunes expired sessions", %{
    conn: conn,
    opts: opts
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)
    Application.put_env(:copi, :session_ttl_seconds, 3600)

    Repo.insert!(%SessionRecord{
      id: "expired-session",
      data: "expired",
      expires_at: DateTime.add(DateTime.utc_now(), -1, :second)
    })

    first_session = %{
      "resume_player_session" => [
        %{"game_id" => "game-1", "player_id" => "player-1"}
      ]
    }

    first_cookie = SessionStore.put(conn, nil, first_session, opts)

    refute Repo.get(SessionRecord, "expired-session")

    [record] = Repo.all(SessionRecord)
    record_id = record.id
    assert binary_part(record.data, 0, 4) == "ENC1"
    assert DateTime.compare(record.expires_at, DateTime.utc_now()) == :gt
    assert {^record_id, ^first_session} = SessionStore.get(conn, first_cookie, opts)

    updated_session = %{
      "resume_player_session" => [
        %{"game_id" => "game-2", "player_id" => "player-2"}
      ]
    }

    updated_cookie = SessionStore.put(conn, record_id, updated_session, opts)

    assert Repo.aggregate(SessionRecord, :count) == 1
    assert {^record_id, ^updated_session} = SessionStore.get(conn, updated_cookie, opts)
  end

  test "postgres mode delete removes the backing record", %{conn: conn, opts: opts} do
    Application.put_env(:copi, :postgres_session_store_enabled, true)
    Application.put_env(:copi, :session_ttl_seconds, 3600)

    raw_cookie =
      SessionStore.put(
        conn,
        nil,
        %{"resume_player_session" => [%{"game_id" => "game", "player_id" => "player"}]},
        opts
      )

    session_id = postgres_session_id(conn, raw_cookie, opts)

    assert SessionStore.delete(conn, session_id, opts) == nil
    refute Repo.get(SessionRecord, session_id)
  end

  test "postgres mode returns an empty session when the cookie is missing", %{
    conn: conn,
    opts: opts
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)

    assert {nil, %{}} = SessionStore.get(conn, nil, opts)
  end

  test "postgres mode returns an empty session when the record is missing", %{
    conn: conn,
    opts: opts
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)

    raw_cookie = postgres_cookie(conn, opts, "missing-session")

    assert {nil, %{}} = SessionStore.get(conn, raw_cookie, opts)
  end

  test "postgres mode returns an empty session when the record is expired", %{
    conn: conn,
    opts: opts
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)

    Repo.insert!(%SessionRecord{
      id: "expired-session",
      data: "expired",
      expires_at: DateTime.add(DateTime.utc_now(), -1, :second)
    })

    raw_cookie = postgres_cookie(conn, opts, "expired-session")

    assert {nil, %{}} = SessionStore.get(conn, raw_cookie, opts)
  end

  test "postgres mode returns an empty session when the payload cannot be decrypted", %{
    conn: conn,
    opts: opts
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)

    Repo.insert!(%SessionRecord{
      id: "undecryptable-session",
      data: "not-encrypted",
      expires_at: DateTime.add(DateTime.utc_now(), 3600, :second)
    })

    raw_cookie = postgres_cookie(conn, opts, "undecryptable-session")

    assert {nil, %{}} = SessionStore.get(conn, raw_cookie, opts)
  end

  test "postgres mode returns an empty session when decrypted data is not a serialized term", %{
    conn: conn,
    opts: opts
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)

    {:ok, invalid_term_blob} = EncryptedBinary.encrypt("not an erlang term")

    Repo.insert!(%SessionRecord{
      id: "invalid-term-session",
      data: invalid_term_blob,
      expires_at: DateTime.add(DateTime.utc_now(), 3600, :second)
    })

    raw_cookie = postgres_cookie(conn, opts, "invalid-term-session")

    assert {nil, %{}} = SessionStore.get(conn, raw_cookie, opts)
  end

  defp postgres_cookie(conn, opts, session_id) do
    Plug.Session.COOKIE.put(conn, nil, %{"postgres_session_id" => session_id}, opts.cookie)
  end

  defp postgres_session_id(conn, raw_cookie, opts) do
    {_cookie_id, %{"postgres_session_id" => session_id}} =
      Plug.Session.COOKIE.get(conn, raw_cookie, opts.cookie)

    session_id
  end

  defp restore_env(key, nil), do: Application.delete_env(:copi, key)
  defp restore_env(key, value), do: Application.put_env(:copi, key, value)
end
