defmodule Copi.Repo.Migrations.CreateContinueVotes do
  use Ecto.Migration

  def change do
    create table(:continue_votes) do
      add :player_id, references(:players, type: :uuid, on_delete: :delete_all), null: false
      add :game_id, references(:games, type: :uuid, on_delete: :delete_all), null: false

      timestamps()
    end

    create index(:continue_votes, [:player_id])
    create index(:continue_votes, [:game_id])
    create unique_index(:continue_votes, [:player_id, :game_id], name: :continue_votes_player_id_game_id_index)
  end
end