defmodule Copi.Repo.Migrations.CreateCards do
  use Ecto.Migration

  def change do
    create table(:cards) do
      add :category, :string
      add :value, :string
      add :description, :text
      add :misc, :string
      add :edition, :string
      add :language, :string
      add :version, :string
      add :owasp_scp, {:array, :string}
      add :owasp_asvs, {:array, :string}
      add :owasp_masvs, {:array, :string}, default: []
      add :owasp_mastg, {:array, :string}
      add :owasp_appsensor, {:array, :string}
      add :capec, {:array, :string}
      add :safecode, {:array, :string}
      add :url, :string, default: ""
      timestamps()
    end

  end
end
