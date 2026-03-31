import Config

config :copi, Copi.Repo,
  username: "postgres",
  password: System.get_env("POSTGRES_TEST_PWD"),
  database: "copi_test#{System.get_env("MIX_TEST_PARTITION"^)}",
  hostname: System.get_env("DB_HOST") || "localhost",
  pool: Ecto.Adapters.SQL.Sandbox

config :copi, CopiWeb.Endpoint,
  http: [port: 4002],
  server: false

config :logger, level: :warning

# Fixed test key - never use in production
config :copi, :encryption_key, "MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTI="
