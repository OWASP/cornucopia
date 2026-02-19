defmodule Copi.Repo.Migrations.AddUniqueConstraintToVotes do
  use Ecto.Migration

  # Disable DDL transaction for concurrent index creation
  @disable_ddl_transaction true

  def up do
    # Remove any existing duplicate votes first
    execute """
    DELETE FROM votes a USING votes b
    WHERE a.id > b.id 
    AND a.player_id = b.player_id 
    AND a.dealt_card_id = b.dealt_card_id
    """

    # Create index concurrently to avoid blocking writes in production
    create unique_index(:votes, [:player_id, :dealt_card_id], 
      name: :votes_player_dealt_card_unique_index,
      concurrently: true)
  end

  def down do
    drop index(:votes, [:player_id, :dealt_card_id],
      name: :votes_player_dealt_card_unique_index)
  end
end
