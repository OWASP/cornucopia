defmodule CopiWebTest do
  use ExUnit.Case, async: true

  test "static_paths returns expected defaults" do
    paths = CopiWeb.static_paths()

    assert "assets" in paths
    assert "images" in paths
    assert "favicon.ico" in paths
  end

  test "__using__/1 can inject controller macros" do
    defmodule ControllerConsumer do
      use CopiWeb, :controller
    end

    assert Code.ensure_loaded?(ControllerConsumer)
    assert function_exported?(ControllerConsumer, :__info__, 1)
  end
end
