defmodule CopiWeb.ErrorHTMLTest do
  use CopiWeb.ConnCase, async: true

  import Phoenix.Template

  test "renders 404.html" do
    assert render_to_string(CopiWeb.ErrorHTML, "404", "html", []) =~ "Nothing here"
  end

  test "renders 500.html and fallback for unknown templates" do
    assert render_to_string(CopiWeb.ErrorHTML, "500", "html", []) =~ "Something went wrong"
    assert render_to_string(CopiWeb.ErrorHTML, "503", "html", []) =~ "Something went wrong"
    assert CopiWeb.ErrorHTML.render("any_template", %{}) =~ "Something went wrong"
  end
end
