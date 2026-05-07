defmodule CopiWeb.HealthControllerTest do
  use CopiWeb.ConnCase

  test "GET /health returns 200 when DB is healthy", %{conn: conn} do
    conn = get(conn, "/health")
    assert response(conn, 200) =~ "healthy"
  end
end
