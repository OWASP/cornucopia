defmodule Copi.Repo.Migrations.AddUniqueConstraintToVotes do
  use Ecto.Migration

  def up do
    # Remove any existing duplicate votes first
    # Use DO $$ block to handle case where table might be empty
    execute """
    DO $$
    BEGIN
      DELETE FROM votes a USING votes b
      WHERE a.id > b.id 
      AND a.player_id = b.player_id 
      AND a.dealt_card_id = b.dealt_card_id;
    EXCEPTION
      WHEN others THEN NULL;
    END $$;
    """

    # Create unique index
    # Note: concurrently option requires @disable_ddl_transaction which
    # can cause issues in test environments, so we use regular index creation
    create unique_index(:votes, [:player_id, :dealt_card_id], 
      name: :votes_player_dealt_card_unique_index)
  end

  def down do
    drop index(:votes, [:player_id, :dealt_card_id],
      name: :votes_player_dealt_card_unique_index)
  end
end
