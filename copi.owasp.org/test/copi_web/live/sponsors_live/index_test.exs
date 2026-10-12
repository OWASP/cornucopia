defmodule CopiWeb.SponsorsLive.IndexTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest

  test "renders the sponsors page", %{conn: conn} do
    {:ok, _view, html} = live(conn, "/sponsors")
    assert is_binary(html)
  end
end
