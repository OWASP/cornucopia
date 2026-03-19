defmodule CopiWeb.PageControllerTest do
  use CopiWeb.ConnCase

  test "GET /", %{conn: conn} do
    conn = get(conn, "/")
    assert html_response(conn, 200) =~ "Threat modelling for everyone everywhere"
  end
end
