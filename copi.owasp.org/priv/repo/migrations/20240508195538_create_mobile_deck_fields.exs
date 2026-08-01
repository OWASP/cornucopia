defmodule Copi.Repo.Migrations.CreateMobileDeckFields do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      Ecto.Migration.remove_if_exists :owasp_masvs, {:array, :string}
      Ecto.Migration.remove_if_exists :owasp_mastg, {:array, :string}
      add :owasp_masvs, {:array, :string}
      add :owasp_mastg, {:array, :string}
    end
  end
end
