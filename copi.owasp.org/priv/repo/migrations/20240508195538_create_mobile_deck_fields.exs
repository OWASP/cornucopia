defmodule Copi.Repo.Migrations.CreateMobileDeckFields do
  use Ecto.Migration

  def change do
    alter table(:card) do
      add :owasp_masvs, {:array, :string}, default: nil
      add :owasp_mastg, {:array, :string}, default: nil
    end
  end
end
