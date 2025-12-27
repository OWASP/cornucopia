# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
import Config

config :copi,
  ecto_repos: [Copi.Repo],
  generators: [timestamp_type: :utc_datetime]

# Configures the endpoint
config :copi, CopiWeb.Endpoint,
  debug_errors: false,
  url: [host: "localhost"],
  secret_key_base: "LgvNRXYWe539tFQXsMkDuRniXGaiEzTMWUj2GIanun0dlbtV6vPlTGZ/l8qR1V7f",
  adapter: Bandit.PhoenixAdapter,
  render_errors: [
    formats: [html: CopiWeb.ErrorHTML, json: CopiWeb.ErrorJSON],
    root_layout: {CopiWeb.ErrorHTML, :root},
    layout: false
  ],
  pubsub_server: Copi.PubSub,
  live_view: [signing_salt: "41WxPtFA"]

config :copi, env: Mix.env()

# Configure rate limiting to prevent abuse (CAPEC 212 - Functionality Misuse)
config :copi, Copi.RateLimiter,
  # Maximum number of games that can be created from a single IP in the time window
  max_games_per_ip: System.get_env("MAX_GAMES_PER_IP", "10") |> String.to_integer(),
  # Time window in seconds for game creation rate limiting (default: 1 hour)
  game_creation_window_seconds: System.get_env("GAME_CREATION_WINDOW_SECONDS", "3600") |> String.to_integer(),
  # Maximum number of WebSocket connections from a single IP in the time window
  max_connections_per_ip: System.get_env("MAX_CONNECTIONS_PER_IP", "50") |> String.to_integer(),
  # Time window in seconds for connection rate limiting (default: 5 minutes)
  connection_window_seconds: System.get_env("CONNECTION_WINDOW_SECONDS", "300") |> String.to_integer()

# Configure tailwind (the version is required)
config :tailwind,
  version: "3.4.0",
  copi: [
    args: ~w(
      --config=tailwind.config.js
      --input=css/app.css
      --output=../priv/static/assets/css/app.css
    ),
    cd: Path.expand("../assets", __DIR__)
  ]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{config_env()}.exs"
