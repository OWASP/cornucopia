defmodule CopiWeb.Plugs.RateLimiterTest do
  use CopiWeb.ConnCase, async: true

  alias CopiWeb.Plugs.RateLimiter
  alias Copi.RateLimiter, as: RateLimiterServer

  setup do
    # Clear any existing state
    RateLimiterServer.clear_ip("127.0.0.1")
    :ok
  end

  describe "rate limiter plug" do
    test "allows requests under the limit", %{conn: conn} do
      conn = RateLimiter.call(conn, action: :game_creation)
      
      refute conn.halted
      assert get_resp_header(conn, "x-ratelimit-remaining") != []
    end

    test "blocks requests over the limit", %{conn: conn} do
      config = RateLimiterServer.get_config()
      max_requests = config.game_creation.max_requests
      
      # Exhaust the rate limit
      for _i <- 1..max_requests do
        RateLimiterServer.check_rate("127.0.0.1", :game_creation)
        RateLimiterServer.record_action("127.0.0.1", :game_creation)
      end
      
      # Next request should be blocked
      conn = RateLimiter.call(conn, action: :game_creation)
      
      assert conn.halted
      assert conn.status == 429
      assert get_resp_header(conn, "retry-after") != []
      assert get_resp_header(conn, "x-ratelimit-remaining") == ["0"]
    end

    test "sets rate limit headers", %{conn: conn} do
      conn = RateLimiter.call(conn, action: :game_creation)
      
      headers = get_resp_header(conn, "x-ratelimit-remaining")
      assert length(headers) > 0
      
      [remaining] = headers
      assert String.to_integer(remaining) >= 0
    end

    test "handles different actions separately", %{conn: conn} do
      # Test game creation
      conn1 = RateLimiter.call(conn, action: :game_creation)
      refute conn1.halted
      
      # Test connection (should be independent)
      conn2 = RateLimiter.call(conn, action: :connection)
      refute conn2.halted
    end
  end
end
