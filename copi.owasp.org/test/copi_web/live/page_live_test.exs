defmodule CopiWeb.PageLiveTest do
  use CopiWeb.ConnCase



  test "Front page", %{conn: conn} do
    assert html_response(get(conn, "/"), 200) =~ "Threat modelling for everyone everywhere"
  end
end
