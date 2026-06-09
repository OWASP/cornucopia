defmodule Copi.Repo.Migrations.AlterMiscToText do
  use Ecto.Migration

  def up do
    alter table(:cards) do
      modify :misc, :text
    end
  end

  def down do
    alter table(:cards) do
      modify :misc, :string
    end
  end
end