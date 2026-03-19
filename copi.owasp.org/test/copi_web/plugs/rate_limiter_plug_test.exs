defmodule CopiWeb.Plugs.RateLimiterPlugTest do
  use ExUnit.Case, async: false
  use Plug.Test

  alias CopiWeb.Plugs.RateLimiterPlug
  alias Copi.RateLimiter

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

    # Inject pre-exhausted timestamps directly to avoid relying on the
    # 1-second sliding window, which can expire under CI load with 133 calls.
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
  end

  test "skips rate limiting when only remote IP is available" do
    ip = {127, 0, 0, 1}
    config = RateLimiter.get_config()
    limit = config.limits.connection

    # Exhaust the limit on RateLimiter manually
    for _ <- 1..limit do
      RateLimiter.check_rate(ip, :connection)
    end

    # The plug should still let it through because it skips non-forwarded IPs
    conn =
      conn(:get, "/")
      |> Map.put(:remote_ip, ip)
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    refute conn.halted
  end

  test "skips rate limiting when no IP info is available" do
    # Explicitly set remote_ip to nil so get_ip_source returns {:none, nil}
    conn =
      conn(:get, "/")
      |> Map.put(:remote_ip, nil)
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    refute conn.halted
  end

  test "init/1 passes opts through unchanged" do
    assert RateLimiterPlug.init([]) == []
    assert RateLimiterPlug.init(foo: :bar) == [foo: :bar]
  end

  test "skips rate limiting when remote_ip is explicitly nil" do
    # Explicitly nil remote_ip + no forwarded header → {:none, nil} branch
    conn =
      conn(:get, "/")
      |> Map.put(:remote_ip, nil)
      |> init_test_session(%{})
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    refute conn.halted
  end
end
