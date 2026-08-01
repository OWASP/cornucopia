defmodule CopiWeb.HealthControllerTest do
  use CopiWeb.ConnCase

  defmodule RepoStub do
    def query(_sql, _params, _opts) do
      case Application.get_env(:copi, :health_repo_stub_mode, :ok) do
        :ok -> {:ok, :ok}
        :raise -> raise "boom"
        :throw -> throw(:boom)
      end
    end
  end

  setup do
    old_repo_mod = Application.get_env(:copi, :health_repo_module)
    old_mode = Application.get_env(:copi, :health_repo_stub_mode)

    on_exit(fn ->
      Application.put_env(:copi, :health_repo_module, old_repo_mod)
      Application.put_env(:copi, :health_repo_stub_mode, old_mode)
    end)

    :ok
  end

  test "GET /health returns 200 when DB is healthy", %{conn: conn} do
    conn = get(conn, "/health")
    assert response(conn, 200) =~ "healthy"
  end

  test "index returns 503 when repo query raises", %{conn: conn} do
    Application.put_env(:copi, :health_repo_module, RepoStub)
    Application.put_env(:copi, :health_repo_stub_mode, :raise)

    conn = CopiWeb.HealthController.index(conn, %{})
    assert response(conn, 503) =~ "not ready"
  end

  test "index returns 503 when repo query throws", %{conn: conn} do
    Application.put_env(:copi, :health_repo_module, RepoStub)
    Application.put_env(:copi, :health_repo_stub_mode, :throw)

    conn = CopiWeb.HealthController.index(conn, %{})
    assert response(conn, 503) =~ "not ready"
  end
end
