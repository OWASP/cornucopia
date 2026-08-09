defmodule Copi.Repo.Migrations.AddUniqueConstraintToVotes do
  use Ecto.Migration

  def change do
    create unique_index(:votes, [:player_id, :dealt_card_id], name: :votes_player_id_dealt_card_id_index)
  end
end