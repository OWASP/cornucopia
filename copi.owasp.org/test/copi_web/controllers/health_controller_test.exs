defmodule CopiWeb.HealthControllerTest do
  use CopiWeb.ConnCase

  test "GET /health returns 200 when database is up", %{conn: conn} do
    conn = get(conn, "/health")
    assert conn.status == 200
    assert conn.resp_body == "healthy\n"
  end

  test "GET /health returns valid response", %{conn: conn} do
    conn = get(conn, "/health")
    assert conn.status in [200, 503]
  end
end
