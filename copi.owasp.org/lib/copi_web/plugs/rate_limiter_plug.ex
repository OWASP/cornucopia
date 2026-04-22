defmodule CopiWeb.Plugs.RateLimiterPlug do
  import Plug.Conn
  require Logger
  alias Copi.RateLimiter
  alias Copi.IPHelper

  def init(opts), do: opts

  def call(conn, opts) do
    action = Keyword.get(opts, :action, :connection)

    case IPHelper.get_ip_source(conn) do
      {:forwarded, ip} ->
        # Only enforce rate limits when we have a forwarded
        # client IP (left-most value from X-Forwarded-For). This avoids
        # rate-limiting on internal/transport addresses injected by the
        # reverse proxy or adapter.
        case RateLimiter.check_rate(ip, action) do
          {:ok, _remaining} ->
            if action == :connection do
              # Persist the chosen client IP into the session so LiveView
              # receives it on websocket connect (connect_info.session).
              put_session(conn, "client_ip", IPHelper.ip_to_string(ip))
            else
              conn
            end

          {:error, :rate_limit_exceeded} ->
            Logger.warning("Rate limit exceeded for IP: #{inspect(ip)} on action #{action}")

            conn
            |> put_resp_content_type(content_type_for(action))
            |> send_resp(429, response_body_for(action))
            |> halt()
        end

      {:remote, _ip} ->
        # We only have a transport (remote) IP; skip rate limiting
        # to avoid false positives caused by proxies or adapter internals.
        Logger.debug("Skipping rate limiting: only transport IP available")
        conn

      {:none, _} ->
        # No IP information available; be permissive and continue.
        Logger.debug("No IP information available for connection; skipping rate limiting")
        conn
    end
  end

  defp content_type_for(:connection), do: "text/plain"
  defp content_type_for(_action), do: "application/json"

  defp response_body_for(:connection), do: "Too many connections, try again later."
  defp response_body_for(_action), do: ~s({"error":"Rate limit exceeded. Please try again later."})
end
