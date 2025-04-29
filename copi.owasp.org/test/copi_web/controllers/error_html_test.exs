defmodule CopiWeb.ErrorHTMLTest do
  use CopiWeb.ConnCase, async: true

  # Bring render_to_string/4 for testing custom views
  import Phoenix.Template


  test "renders 404.html" do
    assert render_to_string(CopiWeb.ErrorHTML, "404", "html", []) =~ "Nothing here"
  end

  test "renders 500.html" do
    assert render_to_string(CopiWeb.ErrorHTML, "500", "html", []) =~ "Something went wrong"
  end
end
