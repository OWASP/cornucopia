defmodule CopiWeb.HealthControllerTest do
  use CopiWeb.ConnCase

  test "GET /health returns 200 when database is available", %{conn: conn} do
    conn = get(conn, "/health")
    assert conn.status == 200
    assert conn.resp_body == "healthy\n"
  end
end
