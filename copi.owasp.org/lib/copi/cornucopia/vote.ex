defmodule Copi.Cornucopia.Vote do
  use Ecto.Schema

  schema "votes" do
    belongs_to :player, Copi.Cornucopia.Player, type: Ecto.ULID
    belongs_to :dealt_card, Copi.Cornucopia.DealtCard

    timestamps()
  end
end
