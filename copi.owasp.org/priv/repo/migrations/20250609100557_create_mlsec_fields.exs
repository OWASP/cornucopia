defmodule Copi.Repo.Migrations.CreateMlSecFields do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      Ecto.Migration.remove_if_exists :biml, :string
      add :biml, :string
    end
  end
end
