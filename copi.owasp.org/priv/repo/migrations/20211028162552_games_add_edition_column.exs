defmodule Copi.Repo.Migrations.GamesAddEditionColumn do
  use Ecto.Migration

  def change do
    alter table("games") do
      add :edition, :string, default: "ecommerce"
    end
  end
end
