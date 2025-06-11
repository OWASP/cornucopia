defmodule Copi.Repo.Migrations.CreateMobileDeckFields do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      Ecto.Migration.remove_if_exists :owasp_masvs, {:array, :string}, default: []
      Ecto.Migration.remove_if_exists :owasp_mastg, {:array, :string}, default: []
      add :owasp_masvs, {:array, :string}, default: []
      add :owasp_mastg, {:array, :string}, default: []
    end
  end
end
