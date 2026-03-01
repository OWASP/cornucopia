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
    config = RateLimiter.get_config()
    limit = config.limits.connection

    # Exhaust the limit first
    for _ <- 1..limit do
      RateLimiter.check_rate(ip, :connection)
    end

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
    # No headers, no remote_ip
    conn =
      conn(:get, "/")
      |> RateLimiterPlug.call([])

    assert conn.status != 429
    refute conn.halted
  end
end
