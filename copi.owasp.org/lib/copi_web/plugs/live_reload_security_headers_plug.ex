defmodule CopiWeb.Plugs.LiveReloadSecurityHeadersPlug do
  import Plug.Conn

  alias CopiWeb.SecurityHeaders

  def init(opts), do: opts

  def call(conn, _opts) do
    if live_reload_request?(conn) do
      Enum.reduce(SecurityHeaders.live_reload_headers(), conn, fn {header, value}, acc ->
        put_resp_header(acc, header, value)
      end)
    else
      conn
    end
  end

  defp live_reload_request?(%Plug.Conn{path_info: ["phoenix", "live_reload" | _]}), do: true
  defp live_reload_request?(_conn), do: false
end