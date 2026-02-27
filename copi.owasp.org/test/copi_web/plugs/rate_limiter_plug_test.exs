defmodule CopiWeb.Plugs.RateLimiterPlugTest do
  use CopiWeb.ConnCase, async: false

  alias CopiWeb.Plugs.RateLimiterPlug

  test "init returns options unchanged" do
    assert RateLimiterPlug.init([]) == []
  end

  test "skips processing if conn already halted" do
    conn =
      build_conn()
      |> Map.put(:halted, true)

    conn = RateLimiterPlug.call(conn, [])

    assert conn.halted
  end

  test "calls plug normally without exceeding limit" do
    conn = build_conn()
    conn = RateLimiterPlug.call(conn, [])

    refute conn.halted
  end

  test "allows request with X-Forwarded-For header within rate limit" do
    conn =
      build_conn()
      |> put_req_header("x-forwarded-for", "1.2.3.4")

    conn = RateLimiterPlug.call(conn, [])

    # Should not be halted - rate limit not yet exceeded
    refute conn.halted
  end

  test "returns 429 when X-Forwarded-For IP exceeds rate limit" do
    # The connection rate limit is 133/window. Exhaust it programmatically.
    unique_ip = {33, 44, 55, 66}
    ip_string = "33.44.55.66"

    # Directly exhaust the rate limit. 133 is the default limit, so after
    # 134 calls the next one will be rejected.
    Enum.each(1..134, fn _ ->
      Copi.RateLimiter.check_rate(unique_ip, :connection)
    end)

    # Now the next request should be rate limited
    conn =
      build_conn()
      |> put_req_header("x-forwarded-for", ip_string)

    result = RateLimiterPlug.call(conn, [])

    # Should be halted with 429
    assert result.halted
  end

  test "skips rate limiting for remote-only IP (no forwarded header)" do
    # build_conn() has a remote_ip but no X-Forwarded-For
    # so get_ip_source returns {:remote, ip} which skips rate limiting
    conn = build_conn()
    result = RateLimiterPlug.call(conn, [])
    refute result.halted
  end
end
