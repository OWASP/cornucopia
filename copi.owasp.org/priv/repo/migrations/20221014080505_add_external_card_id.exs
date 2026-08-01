defmodule Copi.Repo.Migrations.AddExternalCardId do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      add :external_id, :string, default: ""
    end
  end
end
