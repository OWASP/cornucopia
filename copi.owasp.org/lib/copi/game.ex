defmodule Copi.Game do
  use Ecto.Schema
  import Ecto.Changeset

  schema "games" do
    field :created_at, :utc_datetime
    field :finished_at, :utc_datetime
    field :name, :string
    field :started_at, :utc_datetime

    timestamps()
  end

  @doc false
  def changeset(game, attrs) do
    game
    |> cast(attrs, [:name, :created_at, :started_at, :finished_at])
    |> validate_required([:name, :created_at, :started_at, :finished_at])
  end
end
