defmodule CopiWeb.GettextTest do
  use ExUnit.Case, async: true
  
  test "gettext backend is configured" do
    # Verify the module exists and uses Gettext
    assert function_exported?(CopiWeb.Gettext, :__gettext__, 1)
  end

  test "can use gettext for translations" do
    import CopiWeb.Gettext
    
    # Basic usage should not crash
    result = gettext("test")
    assert is_binary(result)
  end

  test "handles interpolation" do
    import CopiWeb.Gettext
    
    # Should handle missing translations gracefully
    result = gettext("Hello %{name}", name: "World")
    assert is_binary(result)
  end

  test "dgettext works with domains" do
    import CopiWeb.Gettext
    
    result = dgettext("errors", "test error")
    assert is_binary(result)
  end

  test "ngettext handles plurals" do
    import CopiWeb.Gettext
    
    result = ngettext("one item", "%{count} items", 1)
    assert is_binary(result)
    
    result_plural = ngettext("one item", "%{count} items", 5)
    assert is_binary(result_plural)
  end
end
