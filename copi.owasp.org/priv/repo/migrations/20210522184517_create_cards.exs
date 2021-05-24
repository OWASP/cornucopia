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
      add :owasp_scp, :string
      add :owasp_asvs, :string
      add :owasp_appsensor, :string
      add :capec, :string
      add :safecode, :string

      timestamps()
    end

  end
end
