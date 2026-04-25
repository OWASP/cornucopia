defmodule CopiWeb.HealthController do
  use CopiWeb, :controller
  require Logger

  def index(conn, _params) do
    # Check database connection with timeouts and exception handling
    try do
      {:ok, _} = Copi.Repo.query("SELECT 1", [], timeout: 1_000, pool_timeout: 1_000)
      send_resp(conn, :ok, "healthy\n")
    rescue
      _ -> send_resp(conn, :service_unavailable, "not ready\n")
    catch
      _, _ -> send_resp(conn, :service_unavailable, "not ready\n")
    end
  end
end
