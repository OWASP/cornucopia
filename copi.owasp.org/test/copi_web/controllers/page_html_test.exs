defmodule CopiWeb.PageHTMLTest do
  use ExUnit.Case, async: true

  test "module exists and uses Phoenix.Component" do
    assert function_exported?(CopiWeb.PageHTML, :__components__, 0)
  end

  test "home template is available" do
    # The embed_templates should make home available
    assert function_exported?(CopiWeb.PageHTML, :home, 1)
  end
end
