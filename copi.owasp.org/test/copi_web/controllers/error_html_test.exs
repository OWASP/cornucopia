defmodule CopiWeb.ErrorHTMLTest do
  use CopiWeb.ConnCase, async: true

  import Phoenix.Template

  test "renders 404.html" do
    assert render_to_string(CopiWeb.ErrorHTML, "404", "html", []) =~ "Nothing here"
  end

  test "renders 500.html and fallback for unknown templates" do
    assert render_to_string(CopiWeb.ErrorHTML, "500", "html", []) =~ "Something went wrong"
    assert render_to_string(CopiWeb.ErrorHTML, "503", "html", []) =~ "Something went wrong"
  end

  test "render/2 falls back to 500 template for unknown error codes" do
    # render_to_string routes through our custom render/2 catch-all for
    # template names that have no embedded-template match (e.g. 418).
    assert render_to_string(CopiWeb.ErrorHTML, "418", "html", []) =~ "Something went wrong"
  end
end
