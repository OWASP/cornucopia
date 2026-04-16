defmodule CopiWeb.HealthControllerTest do
  use CopiWeb.ConnCase, async: true

  test "GET /health returns 200 healthy when database is up", %{conn: conn} do
    conn = get(conn, "/health")
    assert response(conn, 200) =~ "healthy"
  end

  test "direct HealthController.index call traces correctly", %{conn: conn} do
    res = CopiWeb.HealthController.index(conn, %{})
    assert res.status in [200, 503]
  end
end
