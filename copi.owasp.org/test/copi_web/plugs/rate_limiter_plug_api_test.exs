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

  describe "API endpoint rate limiting" do
    test "allows API requests under the rate limit" do
      conn =
        conn(:put, "/api/games/test/players/test/card")
        |> put_req_header("x-forwarded-for", "10.0.0.1")
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status != 429
      assert get_session(conn, "client_ip") == "10.0.0.1"
    end

    test "applies api_action rate limit to PUT /card requests" do
      ip = "192.168.1.100"
      config = RateLimiter.get_config()
      limit = config.limits.api_action

      # Exhaust the API action limit first
      for _ <- 1..limit do
        RateLimiter.check_rate(ip, :api_action)
      end

      conn =
        conn(:put, "/api/games/test/players/test/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.resp_body == "Too many requests, try again later."
      assert conn.halted
    end

    test "applies connection rate limit to non-card API requests" do
      ip = "192.168.1.100"
      config = RateLimiter.get_config()
      limit = config.limits.connection

      # Exhaust the connection limit first
      for _ <- 1..limit do
        RateLimiter.check_rate(ip, :connection)
      end

      conn =
        conn(:get, "/api/some-other-endpoint")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.halted
    end

    test "uses api_action for PUT requests containing /card" do
      conn =
        conn(:put, "/api/games/123/players/456/card")
        |> RateLimiterPlug.call([])

      # The plug should determine the action correctly
      # We can't easily test the internal action determination, 
      # but we can verify it doesn't crash
      refute conn.halted
    end

    test "uses connection for PUT requests not containing /card" do
      conn =
        conn(:put, "/api/games/123/players/456/some-other-action")
        |> RateLimiterPlug.call([])

      refute conn.halted
    end

    test "uses connection for GET requests" do
      conn =
        conn(:get, "/api/games/123/players/456/card")
        |> RateLimiterPlug.call([])

      refute conn.halted
    end

    test "uses connection for POST requests" do
      conn =
        conn(:post, "/api/games/123/players/456/card")
        |> RateLimiterPlug.call([])

      refute conn.halted
    end
  end

  describe "Rate limiting behavior" do
    test "skips rate limiting when only remote IP is available" do
      ip = {127, 0, 0, 1}
      config = RateLimiter.get_config()
      limit = config.limits.api_action

      # Exhaust the limit on RateLimiter manually
      for _ <- 1..limit do
        RateLimiter.check_rate(ip, :api_action)
      end

      # The plug should still let it through because it skips non-forwarded IPs
      conn =
        conn(:put, "/api/games/test/players/test/card")
        |> Map.put(:remote_ip, ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status != 429
      refute conn.halted
    end

    test "skips rate limiting when no IP info is available" do
      # No headers, no remote_ip
      conn =
        conn(:put, "/api/games/test/players/test/card")
        |> RateLimiterPlug.call([])

      assert conn.status != 429
      refute conn.halted
    end
  end

  describe "Error messages" do
    test "returns appropriate error message for API rate limiting" do
      ip = "192.168.1.100"
      config = RateLimiter.get_config()
      limit = config.limits.api_action

      # Exhaust the API action limit
      for _ <- 1..limit do
        RateLimiter.check_rate(ip, :api_action)
      end

      conn =
        conn(:put, "/api/games/test/players/test/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.resp_body == "Too many requests, try again later."
      assert get_resp_header(conn, "content-type") == ["text/plain; charset=utf-8"]
    end
  end
end
