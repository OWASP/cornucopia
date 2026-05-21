defmodule Copi.ReleaseTest do
  use ExUnit.Case, async: false

  test "release module exports migration tasks" do
    assert function_exported?(Copi.Release, :migrate, 0)
    assert function_exported?(Copi.Release, :rollback, 2)
  end
end
