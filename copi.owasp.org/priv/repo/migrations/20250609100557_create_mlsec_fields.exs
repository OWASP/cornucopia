defmodule Copi.Repo.Migrations.CreateMobileDeckFields do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      add :biml, :string, default: ""
    end
  end
end
