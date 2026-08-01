defmodule Copi.SessionRecord do
  @moduledoc false

  use Ecto.Schema

  @primary_key {:id, :string, autogenerate: false}
  schema "copi_sessions" do
    field :data, :binary
    field :expires_at, :utc_datetime_usec
  end
end
