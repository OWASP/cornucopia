defmodule Copi.RateLimiterEnvTest do
  use ExUnit.Case, async: false

  describe "get_env_config via env vars" do
    test "uses valid RATE_LIMIT env var when set to positive integer" do
      System.put_env("RATE_LIMIT_GAME_CREATION_LIMIT", "5")
      on_exit(fn -> System.delete_env("RATE_LIMIT_GAME_CREATION_LIMIT") end)

      # Restart GenServer to pick up new env var
      pid = Process.whereis(Copi.RateLimiter)
      :ok = GenServer.stop(pid, :normal)
      Process.sleep(200)
      {:ok, _} = Copi.RateLimiter.start_link([])

      config = Copi.RateLimiter.get_config()
      assert config.limits.game_creation == 5
    end

    test "falls back to default when RATE_LIMIT env var is invalid string" do
      System.put_env("RATE_LIMIT_PLAYER_CREATION_LIMIT", "not_a_number")
      on_exit(fn -> System.delete_env("RATE_LIMIT_PLAYER_CREATION_LIMIT") end)

      pid = Process.whereis(Copi.RateLimiter)
      :ok = GenServer.stop(pid, :normal)
      Process.sleep(200)
      {:ok, _} = Copi.RateLimiter.start_link([])

      config = Copi.RateLimiter.get_config()
      assert config.limits.player_creation == 60
    end

    test "falls back to default when RATE_LIMIT env var is zero" do
      System.put_env("RATE_LIMIT_CONNECTION_LIMIT", "0")
      on_exit(fn -> System.delete_env("RATE_LIMIT_CONNECTION_LIMIT") end)

      pid = Process.whereis(Copi.RateLimiter)
      :ok = GenServer.stop(pid, :normal)
      Process.sleep(200)
      {:ok, _} = Copi.RateLimiter.start_link([])

      config = Copi.RateLimiter.get_config()
      assert config.limits.connection == 133
    end

    test "falls back to default when RATE_LIMIT env var is negative" do
      System.put_env("RATE_LIMIT_GAME_CREATION_LIMIT", "-5")
      on_exit(fn -> System.delete_env("RATE_LIMIT_GAME_CREATION_LIMIT") end)

      pid = Process.whereis(Copi.RateLimiter)
      :ok = GenServer.stop(pid, :normal)
      Process.sleep(200)
      {:ok, _} = Copi.RateLimiter.start_link([])

      config = Copi.RateLimiter.get_config()
      assert config.limits.game_creation == 20
    end

    test "restores default state after env tests" do
      pid = Process.whereis(Copi.RateLimiter)
      if pid && Process.alive?(pid) do
        :ok = GenServer.stop(pid, :normal)
        Process.sleep(200)
      end
      {:ok, _} = Copi.RateLimiter.start_link([])
      config = Copi.RateLimiter.get_config()
      assert config.limits.game_creation > 0
    end
  end
end