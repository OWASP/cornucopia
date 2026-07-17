defmodule CopiWeb.Plugs.RateLimiterPlug do
  import Plug.Conn
  require Logger
  alias Copi.RateLimiter
  alias Copi.IPHelper

  def init(opts), do: opts

  def call(conn, _opts) do
    case IPHelper.get_ip_source(conn) do
      {:forwarded, ip} ->
        check_and_limit(conn, ip)

      {:remote, ip} ->
        if fly_mode?() do
          check_and_limit(conn, ip)
        else
          Logger.debug("Skipping connection rate limiting: only transport IP available")
          conn
        end

      {:none, _} ->
        Logger.debug("No IP information available for connection; skipping rate limiting")
        conn
    end
  end

  defp check_and_limit(conn, ip) do
    case RateLimiter.check_rate(ip, :connection) do
      {:ok, _remaining} ->
        put_session(conn, "client_ip", IPHelper.ip_to_string(ip))

      {:error, :rate_limit_exceeded} ->
        Logger.warning("HTTP connection rate limit exceeded for IP: #{inspect(ip)}")
        conn
        |> put_resp_content_type("text/plain")
        |> send_resp(429, "Too many connections, try again later.")
        |> halt()
    end
  end

  defp fly_mode? do
    System.get_env("USE_FLY_CLIENT_IP", "false") |> String.downcase() == "true"
  end
end