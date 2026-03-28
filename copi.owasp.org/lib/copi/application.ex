defmodule Copi.Application do
  @moduledoc false

  use Application

  def start(_type, _args) do
    children = [
      Copi.Vault,
      Copi.Repo,
      CopiWeb.Telemetry,
      {Phoenix.PubSub, name: Copi.PubSub},
      Copi.RateLimiter,
      {DNSCluster, query: Application.get_env(:copi, :dns_cluster_query) || :ignore},
      CopiWeb.Endpoint
    ]

    opts = [strategy: :one_for_one, name: Copi.Supervisor]
    Supervisor.start_link(children, opts)
  end

  def config_change(changed, _new, removed) do
    CopiWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end