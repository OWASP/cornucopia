defmodule CopiWeb.HealthController do
  use CopiWeb, :controller

  def index(conn, _params) do
    # Check database connection with timeouts and exception handling
    try do
      case Copi.Repo.query("SELECT 1", [], timeout: 1_000, pool_timeout: 1_000) do
        {:ok, _} ->
          send_resp(conn, :ok, "healthy\n")
        {:error, _} ->
          send_resp(conn, :service_unavailable, "not ready\n")
      end
    rescue
      _ -> send_resp(conn, :service_unavailable, "not ready\n")
    catch
      :exit, _ -> send_resp(conn, :service_unavailable, "not ready\n")
    end
  end
end
