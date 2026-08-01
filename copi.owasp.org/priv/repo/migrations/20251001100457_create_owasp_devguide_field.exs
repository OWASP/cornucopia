defmodule Copi.Repo.Migrations.CreateOwaspDevguideFields do
  use Ecto.Migration

  def change do
    alter table(:cards) do
      Ecto.Migration.remove_if_exists :owasp_devguide, :string
      add :owasp_devguide, {:array, :string}, default: []
    end
  end
end
