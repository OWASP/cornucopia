defmodule CopiWeb.ResourcesLiveTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest

  test "connected mount works", %{conn: conn} do
    {:ok, _view, html} = live(conn, "/resources")
    assert html =~ "Resources"
    assert html =~ "Articles, blogs, books"
    assert html =~ "Cornucopia game explained"
  end
end
