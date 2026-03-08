defmodule CopiWeb.Plugs.RateLimiterPlugTest do
  use ExUnit.Case, async: false
  use Plug.Test

  alias CopiWeb.Plugs.RateLimiterPlug
  alias Copi.RateLimiter

  setup do
    # Start the RateLimiter GenServer for testing if not already started
    case RateLimiter.start_link([]) do
      {:ok, pid} -> {:ok, pid}
      {:error, {:already_started, pid}} -> {:ok, pid}
    end
    
    RateLimiter.clear_ip_sync({10, 0, 0, 1})
    RateLimiter.clear_ip_sync({192, 168, 1, 100})
    RateLimiter.clear_ip_sync({127, 0, 0, 1})
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
      ip = "192.168.1.100"
      
      # First request should pass
      conn =
        conn(:put, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      refute conn.halted
      
      # Exhaust the api_action rate limit dynamically
      config = RateLimiter.get_config()
      api_limit = config.limits.api_action
      
      for _ <- 1..(api_limit - 1) do
        conn(:put, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])
      end
      
      # Next request should be rate limited
      conn =
        conn(:put, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.halted
    end

    test "uses connection for PUT requests not containing /card" do
      ip = "192.168.1.100"
      
      # Exhaust the connection rate limit dynamically
      config = RateLimiter.get_config()
      conn_limit = config.limits.connection
      
      for _ <- 1..(conn_limit + 2) do
        conn(:put, "/api/games/123/players/456/some-other-action")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])
      end
      
      # Next request should be rate limited
      conn =
        conn(:put, "/api/games/123/players/456/some-other-action")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.halted
    end

    test "uses connection for GET requests" do
      ip = "192.168.1.100"
      
      # Exhaust the connection rate limit dynamically
      config = RateLimiter.get_config()
      conn_limit = config.limits.connection
      
      for _ <- 1..(conn_limit + 2) do
        conn(:get, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])
      end
      
      # Next request should be rate limited
      conn =
        conn(:get, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.halted
    end

    test "uses connection for POST requests" do
      ip = "192.168.1.100"
      
      # Exhaust the connection rate limit dynamically
      config = RateLimiter.get_config()
      conn_limit = config.limits.connection
      
      for _ <- 1..(conn_limit + 2) do
        conn(:post, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])
      end
      
      # Next request should be rate limited
      conn =
        conn(:post, "/api/games/123/players/456/card")
        |> put_req_header("x-forwarded-for", ip)
        |> init_test_session(%{})
        |> RateLimiterPlug.call([])

      assert conn.status == 429
      assert conn.halted
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
