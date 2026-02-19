defmodule Copi.Repo.Migrations.AddUniqueConstraintToVotes do
  use Ecto.Migration

  def change do
    # Remove any existing duplicate votes first
    execute """
    DELETE FROM votes a USING votes b
    WHERE a.id > b.id 
    AND a.player_id = b.player_id 
    AND a.dealt_card_id = b.dealt_card_id
    """

    create unique_index(:votes, [:player_id, :dealt_card_id], 
      name: :votes_player_dealt_card_unique_index)
  end
end
