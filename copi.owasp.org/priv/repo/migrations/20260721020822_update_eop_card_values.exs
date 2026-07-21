defmodule Copi.Repo.Migrations.UpdateEopCardValues do
  use Ecto.Migration

  def change do
    execute(
      "UPDATE cards SET value = '10' WHERE edition = 'eop' AND value = 'X'",
      "UPDATE cards SET value = 'X' WHERE edition = 'eop' AND value = '10'"
    )
  end
end
