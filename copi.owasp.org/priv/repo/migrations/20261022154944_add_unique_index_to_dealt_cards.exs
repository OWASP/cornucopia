defmodule Copi.Repo.Migrations.AddUniqueIndexToDealtCards do
  use Ecto.Migration

  def change do
    # Remove duplicate (card_id, player_id) pairs introduced by the race condition,
    # preserving the row with the lowest id and deleting its votes first to satisfy
    # the foreign key constraint on votes.dealt_card_id.
    execute(
      """
      DELETE FROM votes
      WHERE dealt_card_id IN (
        SELECT id FROM dealt_cards
        WHERE id NOT IN (
          SELECT MIN(id) FROM dealt_cards GROUP BY card_id, player_id
        )
      )
      """,
      ""
    )

    execute(
      """
      DELETE FROM dealt_cards
      WHERE id NOT IN (
        SELECT MIN(id) FROM dealt_cards GROUP BY card_id, player_id
      )
      """,
      ""
    )

    drop index(:dealt_cards, [:card_id])
    create unique_index(:dealt_cards, [:card_id, :player_id])
  end
end