import Config

if System.get_env("PHX_SERVER") do
  config :copi, CopiWeb.Endpoint, server: true
end

ssl_verify = if System.get_env("ECTO_SSL_VERIFY") in ~w(false 0), do: [ verify: :verify_none], else: false

if config_env() == :prod do
  database_url =
    System.get_env("DATABASE_URL") ||
      raise """
      environment variable DATABASE_URL is missing.
      For example: ecto://USER:PASS@HOST/DATABASE
      """

  maybe_ipv6 = if System.get_env("ECTO_IPV6") in ~w(true 1), do: [:inet6], else: [:inet, :inet6]

  config :copi, Copi.Repo,
    ssl: ssl_verify,
    url: database_url,
    pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10"),
    socket_options: maybe_ipv6

  secret_key_base =
    System.get_env("SECRET_KEY_BASE") ||
      raise """
      environment variable SECRET_KEY_BASE is missing.
      You can generate one by calling: mix phx.gen.secret
      """

  host = System.get_env("PHX_HOST") || "example.com"
  port = String.to_integer(System.get_env("PORT") || "4000")

  config :copi, :dns_cluster_query, System.get_env("DNS_CLUSTER_QUERY")

  config :copi, CopiWeb.Endpoint,
    url: [host: host, port: 443, scheme: "https"],
    http: [
      ip: {0, 0, 0, 0, 0, 0, 0, 0},
      port: port
    ],
    secret_key_base: secret_key_base

  config :copi, dns_cluster_query: System.get_env("DNS_CLUSTER_QUERY")

  encryption_key =
    System.get_env("COPI_ENCRYPTION_KEY") ||
      raise """
      environment variable COPI_ENCRYPTION_KEY is missing.
      Generate one with:
        elixir -e ':crypto.strong_rand_bytes(32) |> Base.encode64() |> IO.puts()'
      """

  config :copi, Copi.Vault,
    ciphers: [
      default: {
        Cloak.Ciphers.AES.GCM,
        tag: "AES.GCM.V1",
        key: Base.decode64!(encryption_key)
      }
    ]
end