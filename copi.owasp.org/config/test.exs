import Config

config :copi, Copi.Repo,
  username: "postgres",
  password: System.get_env("POSTGRES_TEST_PWD"),
  database: "copi_test#{System.get_env("MIX_TEST_PARTITION")}",
  hostname: System.get_env("DB_HOST") || "localhost",
  pool: Ecto.Adapters.SQL.Sandbox

config :copi, CopiWeb.Endpoint,
  http: [port: 4002],
  server: false

config :logger, level: :warning

config :copi, Copi.Vault,
  ciphers: [
    default: {
      Cloak.Ciphers.AES.GCM,
      tag: "AES.GCM.V1",
      key: Base.decode64!("dGVzdGtleV90ZXN0a2V5X3Rlc3RrZXlfdGVzdGtleSE=")
    }
  ]