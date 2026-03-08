defmodule CopiWeb.Plugs.RateLimiterPlug do
  import Plug.Conn
  require Logger
  alias Copi.RateLimiter
  alias Copi.IPHelper

  def init(opts), do: opts

  def call(conn, _opts) do
    case IPHelper.get_ip_source(conn) do
      {:forwarded, ip} ->
        # Determine action type based on request path and method
        action = determine_action(conn)
        
        # Only enforce connection rate limits when we have a forwarded
        # client IP (left-most value from X-Forwarded-For). This avoids
        # rate-limiting on internal/transport addresses injected by the
        # reverse proxy or adapter.
        case RateLimiter.check_rate(ip, action) do
          {:ok, _remaining} ->
            # Persist the chosen client IP into the session so LiveView
            # receives it on websocket connect (connect_info.session).
            # Only write to session if it's available (stateless API requests won't have sessions)
            if Map.has_key?(conn.private, :plug_session) do
              put_session(conn, "client_ip", IPHelper.ip_to_string(ip))
            else
              conn
            end

          {:error, :rate_limit_exceeded} ->
            Logger.warning("HTTP #{action} rate limit exceeded for IP: #{inspect(ip)}")
            conn
            |> put_resp_content_type("text/plain")
            |> send_resp(429, "Too many requests, try again later.")
            |> halt()
        end

      {:remote, _ip} ->
        # We only have a transport (remote) IP; skip connection rate limiting
        # to avoid false positives caused by proxies or adapter internals.
        Logger.debug("Skipping rate limiting: only transport IP available")
        conn

      {:none, _} ->
        # No IP information available; be permissive and continue.
        Logger.debug("No IP information available for connection; skipping rate limiting")
        conn
    end
  end

  # Determine the action type for rate limiting based on the request
  defp determine_action(conn) do
    case conn.method do
      "PUT" ->
        if String.contains?(conn.request_path, "/card") do
          :api_action
        else
          :connection
        end
      _ ->
        :connection
    end
  end
end
