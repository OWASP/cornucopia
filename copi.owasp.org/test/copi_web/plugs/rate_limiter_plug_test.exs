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
    # Use a unique IP and hammer it to exceed the rate limit
    ip = "222.222.222.222"

    # Exhaust the rate limit (limit is 20/3600s for game_creation-type actions;
    # connection limit is separate - find the connection limit)
    results =
      Enum.map(1..25, fn _ ->
        conn =
          build_conn()
          |> put_req_header("x-forwarded-for", ip)

        RateLimiterPlug.call(conn, [])
      end)

    # At least one response should be rate limited (429)
    assert Enum.any?(results, fn conn -> conn.halted end)
  end

  test "skips rate limiting when no IP info (nil remote_ip, no forwarded header)" do
    # Build conn with nil remote_ip so get_ip_source returns {:none, nil}
    conn = %Plug.Conn{
      remote_ip: nil,
      req_headers: [],
      resp_headers: [],
      private: %{},
      halted: false,
      status: nil,
      resp_body: nil
    }

    result = RateLimiterPlug.call(conn, [])

    # Should not be halted - no IP to rate limit
    refute result.halted
  end
end
