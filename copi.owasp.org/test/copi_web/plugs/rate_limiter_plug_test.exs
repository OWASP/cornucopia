defmodule CopiWeb.Plugs.RateLimiterPlugTest do
  use ExUnit.Case, async: false

  import Plug.Test
  import Plug.Conn

  alias Copi.RateLimiter
  alias CopiWeb.Plugs.RateLimiterPlug

  setup do
    RateLimiter.clear_ip({10, 0, 0, 1})
    RateLimiter.clear_ip({192, 168, 1, 100})
    RateLimiter.clear_ip({127, 0, 0, 1})
    :ok
  end

  test "stores client_ip in session when forwarded IP exists and under limit" do
    conn =
      conn(:get, "/")
      |> put_req_header("x-forwarded-for", "10.0.0.1")
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    assert get_session(conn, "client_ip") == "10.0.0.1"
  end

  test "returns 429 when forwarded IP exceeds connection limit" do
    ip = "192.168.1.100"
    ip_tuple = {192, 168, 1, 100}
    config = RateLimiter.get_config()
    limit = config.limits.connection

    # Seed limiter state directly to make this deterministic under CI timing.
    :sys.replace_state(Copi.RateLimiter, fn state ->
      now = System.monotonic_time(:millisecond)
      timestamps = for _ <- 1..limit, do: now
      new_requests = Map.put(state.requests, {ip_tuple, :connection}, timestamps)
      %{state | requests: new_requests}
    end)

    conn =
      conn(:get, "/")
      |> put_req_header("x-forwarded-for", ip)
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status == 429
    assert conn.resp_body == "Too many connections, try again later."
    assert conn.halted
    assert conn.resp_body =~ "Too many connections"
  end

  test "skips rate limiting when only remote IP is available" do
    ip = {127, 0, 0, 1}
    config = RateLimiter.get_config()
    limit = config.limits.connection

    for _ <- 1..limit do
      RateLimiter.check_rate(ip, :connection)
    end

    conn =
      conn(:get, "/")
      |> Map.put(:remote_ip, ip)
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    refute conn.halted
  end

  test "init/1 returns opts unchanged" do
    opts = [limit: 10, window: 60]
    assert RateLimiterPlug.init(opts) == opts
  end

  test "skips rate limiting when no IP info is available" do
    conn =
      conn(:get, "/")
      |> Map.put(:remote_ip, nil)
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    refute conn.halted
  end
end
