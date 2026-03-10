defmodule CopiWeb.HealthController do
  use CopiWeb, :controller

  def index(conn, _params) do
    # Check database connection
    case Copi.Repo.query("SELECT 1") do
      {:ok, _} ->
        send_resp(conn, :ok, "healthy\n")
      {:error, _} ->
        send_resp(conn, :service_unavailable, "not ready\n")
    end
  end
end
