defmodule CopiWeb.PrivacyLiveTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest

  test "connected mount works", %{conn: conn} do
    {:ok, _view, html} = live(conn, "/privacy")
    assert html =~ "Privacy"
    assert html =~ "What Data Do We Collect"
    assert html =~ "The IP Address Situation"
    assert html =~ "Game Limit"
    assert html =~ "Your Rights"
  end
end
