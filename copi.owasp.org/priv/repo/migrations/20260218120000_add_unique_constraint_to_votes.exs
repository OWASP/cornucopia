defmodule Copi.Repo.Migrations.AddUniqueConstraintToVotes do
  use Ecto.Migration

  def up do
    # Remove any existing duplicate votes first
    # This runs only if votes table has  data
    execute """
    DELETE FROM votes a 
    WHERE a.id IN (
      SELECT a2.id FROM votes a2
      JOIN votes b ON a2.player_id = b.player_id AND a2.dealt_card_id = b.dealt_card_id
      WHERE a2.id > b.id
    )
    """

    # Create unique index
    create unique_index(:votes, [:player_id, :dealt_card_id], 
      name: :votes_player_dealt_card_unique_index)
  end

  def down do
    drop_if_exists index(:votes, [:player_id, :dealt_card_id],
      name: :votes_player_dealt_card_unique_index)
  end
end
