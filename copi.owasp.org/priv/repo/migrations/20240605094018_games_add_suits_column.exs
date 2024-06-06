defmodule Copi.Repo.Migrations.GamesAddSuitsColumn do
  use Ecto.Migration

  def change do
    alter table(:games) do
      add :suits, {:array, :string}, default: []
    end
  end
end
