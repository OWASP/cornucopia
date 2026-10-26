defmodule Copi.Repo.Migrations.AddUniqueIndexToDealtCards do
  use Ecto.Migration

  def change do
    drop index(:dealt_cards, [:card_id])
    create unique_index(:dealt_cards, [:card_id, :player_id])
  end
end