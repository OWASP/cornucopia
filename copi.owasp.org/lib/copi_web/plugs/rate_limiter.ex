defmodule CopiWeb.Plugs.RateLimiter do
  @moduledoc """
  Plug for rate limiting HTTP requests based on IP address.
  """

  import Plug.Conn
  require Logger

  alias Copi.RateLimiter

  def init(opts), do: opts

  def call(conn, opts) do
    action = Keyword.get(opts, :action, :game_creation)
    ip_address = get_ip_address(conn)

    case RateLimiter.check_rate(ip_address, action) do
      {:ok, remaining} ->
        conn
        |> put_resp_header("x-ratelimit-remaining", to_string(remaining))
        
      {:error, :rate_limited, retry_after} ->
        Logger.warning("Rate limit exceeded for IP: #{inspect(ip_address)}, action: #{action}")
        
        conn
        |> put_resp_header("retry-after", to_string(retry_after))
        |> put_resp_header("x-ratelimit-remaining", "0")
        |> send_resp(429, rate_limit_message(action, retry_after))
        |> halt()
    end
  end

  defp get_ip_address(conn) do
    # Try to get real IP from common headers (for reverse proxies)
    case get_req_header(conn, "x-forwarded-for") do
      [forwarded | _] ->
        forwarded
        |> String.split(",")
        |> List.first()
        |> String.trim()

      [] ->
        case conn.remote_ip do
          {a, b, c, d} -> "#{a}.#{b}.#{c}.#{d}"
          {a, b, c, d, e, f, g, h} -> 
            "#{Integer.to_string(a, 16)}:#{Integer.to_string(b, 16)}:#{Integer.to_string(c, 16)}:#{Integer.to_string(d, 16)}:#{Integer.to_string(e, 16)}:#{Integer.to_string(f, 16)}:#{Integer.to_string(g, 16)}:#{Integer.to_string(h, 16)}"
          _ -> "unknown"
        end
    end
  end

  defp rate_limit_message(action, retry_after) do
    action_name = case action do
      :game_creation -> "game creation"
      :connection -> "connections"
      _ -> "requests"
    end

    """
    Rate limit exceeded for #{action_name}.
    Please try again in #{retry_after} seconds.
    
    This protection is in place to ensure service availability for all users.
    """
  end
end
