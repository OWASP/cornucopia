defmodule Copi.Repo.Migrations.CreateMobileDeckFields do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      add :owasp_masvs, {:array, :string}, default: []
      add :owasp_mastg, {:array, :string}, default: []
    end
  end
end
