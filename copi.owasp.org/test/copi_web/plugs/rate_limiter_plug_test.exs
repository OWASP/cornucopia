defmodule CopiWeb.Plugs.RateLimiterPlugTest do
  use CopiWeb.ConnCase, async: false

  alias CopiWeb.Plugs.RateLimiterPlug

  test "init returns options unchanged" do
    assert RateLimiterPlug.init([]) == []
  end

  test "skips processing if conn already halted" do
    conn =
      build_conn()
      |> Map.put(:halted, true)

    conn = RateLimiterPlug.call(conn, [])

    assert conn.halted
  end

  test "calls plug normally without exceeding limit" do
    conn = build_conn()
    conn = RateLimiterPlug.call(conn, [])

    refute conn.halted
  end
end
