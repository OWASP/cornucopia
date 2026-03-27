defmodule Copi.Encrypted.Migrator do
  require Logger

  import Ecto.Query, warn: false

  alias Copi.Repo
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.Player
  alias Copi.Encrypted.Binary, as: EncryptedBinary

  @magic "ENC1"

  def run do
    case System.get_env("COPI_ENCRYPTION_KEY") do
      nil ->
        Logger.warning("[Migrator] Skipping: COPI_ENCRYPTION_KEY is not set")
        {0, 0}

      _ ->
        Logger.info("[Migrator] Starting encryption pass")
        games_count = encrypt_table(Game, :games)
        players_count = encrypt_table(Player, :players)
        Logger.info("[Migrator] Done. Games: #{games_count}, Players: #{players_count}")
        {games_count, players_count}
    end
  end

  defp encrypt_table(schema, label) do
    rows = Repo.all(from r in schema, select: %{id: r.id, name: r.name})

    Enum.reduce(rows, 0, fn %{id: id, name: name}, count ->
      cond do
        is_nil(name) ->
          count

        already_encrypted?(name) ->
          count

        true ->
          {:ok, blob} = EncryptedBinary.encrypt(name)

          Repo.update_all(
            from(r in schema, where: r.id == ^id),
            set: [name: blob]
          )

          Logger.debug("[Migrator] Encrypted #{label} id=#{id}")
          count + 1
      end
    end)
  end

  defp already_encrypted?(<<@magic, _::binary>>), do: true
  defp already_encrypted?(_), do: false
end