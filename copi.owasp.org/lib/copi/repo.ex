defmodule Copi.Repo do
  use Ecto.Repo,
    otp_app: :copi,
    adapter: Ecto.Adapters.Postgres
end
