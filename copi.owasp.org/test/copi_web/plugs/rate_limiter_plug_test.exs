defmodule CopiWeb.Plugs.RateLimiterPlugTest do
  use CopiWeb.ConnCase, async: false

  import Plug.Conn

  alias Copi.RateLimiter
  alias CopiWeb.Plugs.RateLimiterPlug

  setup do
    RateLimiter.clear_ip({127, 0, 0, 1})
    RateLimiter.clear_ip({203, 0, 113, 5})
    :ok
  end

  test "init returns options unchanged" do
    assert RateLimiterPlug.init([]) == []
  end

  test "sets session client_ip when forwarded IP is under limit" do
    conn =
      build_conn()
      |> Plug.Test.init_test_session(%{})
      |> put_req_header("x-forwarded-for", "203.0.113.5")

    conn = RateLimiterPlug.call(conn, [])

    refute conn.halted
    assert get_session(conn, "client_ip") == "203.0.113.5"
  end

  test "halts with 429 when forwarded IP exceeds connection limit" do
    forwarded_ip = {203, 0, 113, 5}
    config = RateLimiter.get_config()

    for _ <- 1..config.limits.connection do
      assert {:ok, _} = RateLimiter.check_rate(forwarded_ip, :connection)
    end

    conn =
      build_conn()
      |> Plug.Test.init_test_session(%{})
      |> put_req_header("x-forwarded-for", "203.0.113.5")

    conn = RateLimiterPlug.call(conn, [])

    assert conn.halted
    assert conn.status == 429
    assert conn.resp_body =~ "Too many connections"
  end

  test "skips rate limiting when only remote transport IP is present" do
    conn = %Plug.Conn{build_conn() | remote_ip: {127, 0, 0, 1}, req_headers: []}

    conn = RateLimiterPlug.call(conn, [])

    refute conn.halted
  end

  test "continues when no IP information is available" do
    conn = %Plug.Conn{build_conn() | remote_ip: nil, req_headers: []}

    conn = RateLimiterPlug.call(conn, [])

    refute conn.halted
  end
end
