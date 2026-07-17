defmodule CopiWeb.PostgresSessionIntegrationTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia
  alias Copi.Encrypted.Binary, as: EncryptedBinary
  alias Copi.PlayerCapabilityConsumption
  alias Copi.PlayerCapabilityRegistry
  alias Copi.Repo
  alias Copi.SessionRecord
  alias CopiWeb.PlayerCapability

  setup do
    previous_value = Application.get_env(:copi, :postgres_session_store_enabled, false)

    on_exit(fn ->
      Application.put_env(:copi, :postgres_session_store_enabled, previous_value)
    end)

    {:ok, game} = Cornucopia.create_game(%{name: "Postgres session game"})
    {:ok, player} = Cornucopia.create_player(%{name: "Postgres player", game_id: game.id})

    %{game: game, player: player}
  end

  test "configured PostgreSQL mode persists the session and rejects replay after local state loss",
       %{
         conn: conn,
         game: game,
         player: player
       } do
    Application.put_env(:copi, :postgres_session_store_enabled, true)
    capability = PlayerCapability.sign(game.id, player.id)

    exchange_response = exchange_capability(conn, game.id, capability)
    clean_path = json_response(exchange_response, 200)["redirect_to"]

    assert clean_path == "/games/#{game.id}/players/#{player.id}"
    assert Repo.aggregate(SessionRecord, :count) == 1
    assert Repo.aggregate(PlayerCapabilityConsumption, :count) == 1

    session_record = Repo.one!(SessionRecord)
    assert binary_part(session_record.data, 0, 4) == "ENC1"
    refute session_record.data =~ game.id
    refute session_record.data =~ player.id

    assert {:ok, plaintext_session} = EncryptedBinary.decrypt(session_record.data)
    database_session = Plug.Crypto.non_executable_binary_to_term(plaintext_session)

    assert database_session["resume_player_session"] == [
             %{"game_id" => game.id, "player_id" => player.id}
           ]

    {:ok, _player_view, player_html} =
      exchange_response
      |> recycle()
      |> live(clean_path)

    assert player_html =~ player.name

    :sys.replace_state(PlayerCapabilityRegistry, fn state ->
      %{state | consumed: %{}}
    end)

    replay_response = exchange_capability(recycle(exchange_response), game.id, capability)
    assert json_response(replay_response, 401)["error"] == "Invalid or expired player capability"
    assert Repo.aggregate(PlayerCapabilityConsumption, :count) == 1
  end

  test "default mode keeps session and replay state out of PostgreSQL", %{
    conn: conn,
    game: game,
    player: player
  } do
    Application.put_env(:copi, :postgres_session_store_enabled, false)
    capability = PlayerCapability.sign(game.id, player.id)

    exchange_response = exchange_capability(conn, game.id, capability)

    assert json_response(exchange_response, 200)["redirect_to"] ==
             "/games/#{game.id}/players/#{player.id}"

    assert Repo.aggregate(SessionRecord, :count) == 0
    assert Repo.aggregate(PlayerCapabilityConsumption, :count) == 0
  end

  defp exchange_capability(conn, game_id, capability) do
    public_response = get(conn, "/games/#{game_id}")
    csrf_token = csrf_token(html_response(public_response, 200))

    public_response
    |> recycle()
    |> put_req_header("x-csrf-token", csrf_token)
    |> post("/api/player-capabilities/exchange", %{"capability" => capability})
  end

  defp csrf_token(html) do
    [_, token] = Regex.run(~r/<meta name="csrf-token" content="([^"]+)"/, html)
    token
  end
end
