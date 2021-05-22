# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

config :copi,
  ecto_repos: [Copi.Repo]

# Configures the endpoint
config :copi, CopiWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "LgvNRXYWe539tFQXsMkDuRniXGaiEzTMWUj2GIanun0dlbtV6vPlTGZ/l8qR1V7f",
  render_errors: [view: CopiWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: Copi.PubSub,
  live_view: [signing_salt: "41WxPtFA"]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
