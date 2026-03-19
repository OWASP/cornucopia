defmodule CopiWeb.GettextTest do
  use ExUnit.Case, async: true
  
  test "gettext backend is configured" do
    # Verify the module exists and uses Gettext
    assert function_exported?(CopiWeb.Gettext, :__gettext__, 1)
  end

  test "gettext module has required functions" do
    # Check that the Gettext backend is properly configured
    assert function_exported?(CopiWeb.Gettext, :lgettext, 4)
    assert function_exported?(CopiWeb.Gettext, :lngettext, 6)
  end
end
