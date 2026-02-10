defmodule Copi.Repo.Migrations.AddRoundOpenToGames do
  use Ecto.Migration

  def change do
    alter table(:games) do
      add :round_open, :boolean, default: true
    end
  end
end