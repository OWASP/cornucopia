defmodule Copi.Repo.Migrations.AddUniqueConstraintsToDealtCards do
  use Ecto.Migration

  def up do
    # Add unique constraint to prevent duplicate card assignments to players
    # This will work now that duplicates have been cleaned up
    create unique_index(:dealt_cards, [:card_id, :player_id], name: :dealt_cards_card_player_unique)
    
    # Log the constraint creation
    execute("""
      DO $$
      BEGIN
        RAISE NOTICE 'Race condition protection: Unique constraints added to dealt_cards';
      END $$;
    """)
  end

  def down do
    drop index(:dealt_cards, :dealt_cards_card_player_unique)
  end
end
