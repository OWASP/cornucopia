defmodule Copi.Repo.Migrations.CleanupDuplicateDealtCards do
  use Ecto.Migration

  def up do
    # First, we need to clean up existing duplicate records caused by the race condition
    # This migration removes duplicates while preserving the earliest occurrence
    
    # Create a temporary table to identify unique records
    execute("""
      CREATE TEMPORARY TABLE unique_dealt_cards AS
      SELECT DISTINCT ON (card_id, player_id) *
      FROM dealt_cards
      ORDER BY card_id, player_id, inserted_at ASC
    """)
    
    # Delete all existing dealt_cards records
    execute("DELETE FROM dealt_cards")
    
    # Re-insert only the unique records
    execute("""
      INSERT INTO dealt_cards 
      SELECT * FROM unique_dealt_cards
    """)
    
    # Drop the temporary table
    execute("DROP TABLE unique_dealt_cards")
    
    # Log the cleanup
    execute("""
      DO $$
      BEGIN
        RAISE NOTICE 'Race condition cleanup completed: Duplicate dealt_cards have been removed';
      END $$;
    """)
  end

  def down do
    # This migration cannot be safely reversed
    # The down migration would require restoring the original duplicate data
    # which would re-introduce the race condition corruption
    raise "Cannot rollback cleanup migration - would restore race condition corruption"
  end
end
