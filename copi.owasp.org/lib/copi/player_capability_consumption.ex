defmodule Copi.PlayerCapabilityConsumption do
  @moduledoc false

  use Ecto.Schema

  @primary_key {:digest, :binary, autogenerate: false}
  schema "player_capability_consumptions" do
    field :expires_at, :utc_datetime_usec
  end
end
