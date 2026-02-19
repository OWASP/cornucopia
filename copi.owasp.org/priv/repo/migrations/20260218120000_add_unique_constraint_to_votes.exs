defmodule Copi.Repo.Migrations.AddUniqueConstraintToVotes do
  use Ecto.Migration

  def up do
    # Remove any existing duplicate votes, keeping only the oldest one
    execute("""
    DELETE FROM votes
    WHERE id NOT IN (
      SELECT MIN(id)
      FROM votes
      GROUP BY player_id, dealt_card_id
    )
    """)

    # Now add the unique constraint
    create unique_index(:votes, [:player_id, :dealt_card_id], 
      name: :votes_player_dealt_card_unique_index)
  end

  def down do
    drop index(:votes, [:player_id, :dealt_card_id], 
      name: :votes_player_dealt_card_unique_index)
  end
end
