defmodule CopiWeb.GameplayFlowTest do
  use CopiWeb.ConnCase, async: false

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia
  alias Copi.Cornucopia.DealtCard
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.Vote
  alias Copi.Repo
  alias CopiWeb.PlayerCapability

  @category "Integration"

  setup do
    {:ok, game} =
      Cornucopia.create_game(%{
        name: "Complete game flow",
        edition: "webapp",
        suits: [@category]
      })

    players =
      for name <- ["Player One", "Player Two", "Player Three"] do
        {:ok, player} = Cornucopia.create_player(%{name: name, game_id: game.id})
        player
      end

    for number <- 1..6 do
      {:ok, _card} =
        Cornucopia.create_card(%{
          category: @category,
          value: Integer.to_string(number),
          description: "Integration card #{number}",
          misc: "integration",
          edition: "webapp",
          external_id: "INTEGRATION_#{number}",
          language: "en",
          version: "3.0",
          owasp_scp: [],
          owasp_devguide: [],
          owasp_asvs: [],
          owasp_appsensor: [],
          capec: [],
          safecode: [],
          owasp_mastg: [],
          owasp_masvs: []
        })
    end

    %{game: game, players: players}
  end

  test "one browser completes a round as three authorized players", %{
    conn: conn,
    game: game,
    players: players
  } do
    browser = exchange_capabilities(conn, game, players)

    public_response = get(browser, "/games/#{game.id}")
    assert html_response(public_response, 200) =~ game.name

    csrf_token = csrf_token(html_response(public_response, 200))
    browser = public_response |> recycle() |> put_req_header("x-csrf-token", csrf_token)

    {:ok, watcher, waiting_html} = live(browser, "/games/#{game.id}")
    assert waiting_html =~ "Start Game"
    render_click(watcher, "start_game", %{})

    {:ok, started_game} = Game.find(game.id)
    assert started_game.started_at

    dealt_cards =
      Map.new(started_game.players, fn player ->
        assert length(player.dealt_cards) == 2
        {player.id, hd(player.dealt_cards)}
      end)

    for player <- players do
      clean_path = "/games/#{game.id}/players/#{player.id}"
      {:ok, _player_view, player_html} = live(browser, clean_path)
      assert player_html =~ player.name

      dealt_card = Map.fetch!(dealt_cards, player.id)

      response =
        put(browser, "/api/games/#{game.id}/players/#{player.id}/card", %{
          "dealt_card_id" => Integer.to_string(dealt_card.id)
        })

      assert json_response(response, 200)["id"] == dealt_card.id
    end

    {:ok, game_after_cards} = Game.find(game.id)

    assert Enum.all?(game_after_cards.players, fn player ->
             Enum.count(player.dealt_cards, &(&1.played_in_round == 1)) == 1
           end)

    [first_player, second_player | _] = players
    second_player_card = Map.fetch!(dealt_cards, second_player.id)

    {:ok, first_player_view, _html} =
      live(browser, "/games/#{game.id}/players/#{first_player.id}")

    render_click(first_player_view, "toggle_vote", %{
      "dealt_card_id" => Integer.to_string(second_player_card.id)
    })

    assert Repo.get_by(Vote,
             player_id: first_player.id,
             dealt_card_id: second_player_card.id
           )

    render_click(first_player_view, "next_round", %{})

    {:ok, round_two_game} = Game.find(game.id)
    assert round_two_game.rounds_played == 1
    assert render(watcher) =~ "Round <strong>2</strong>"
  end

  test "public watching works but an unstored player pair cannot enter or play", %{
    conn: conn,
    game: game,
    players: [authorized_player, unauthorized_player | _]
  } do
    browser = exchange_capabilities(conn, game, [authorized_player])

    public_response = get(browser, "/games/#{game.id}")
    assert html_response(public_response, 200) =~ game.name

    clean_path = "/games/#{game.id}/players/#{unauthorized_player.id}"
    player_response = get(recycle(public_response), clean_path)
    assert redirected_to(player_response, 302) == "/games/#{game.id}"

    dealt_card =
      Repo.insert!(%DealtCard{
        player_id: unauthorized_player.id,
        card_id: create_extra_card!().id
      })

    csrf_token = csrf_token(html_response(public_response, 200))

    card_response =
      public_response
      |> recycle()
      |> put_req_header("x-csrf-token", csrf_token)
      |> put("/api/games/#{game.id}/players/#{unauthorized_player.id}/card", %{
        "dealt_card_id" => Integer.to_string(dealt_card.id)
      })

    assert json_response(card_response, 401)["error"] == "Valid player session required"
    assert Repo.reload(dealt_card).played_in_round == nil
  end

  defp exchange_capabilities(conn, game, players) do
    Enum.reduce(players, conn, fn player, browser ->
      capability = PlayerCapability.sign(game.id, player.id)
      response =
        post(browser, "/api/player-capabilities/exchange", %{"capability" => capability})

      clean_path = json_response(response, 200)["redirect_to"]
      assert clean_path == "/games/#{game.id}/players/#{player.id}"
      refute clean_path =~ capability

      recycle(response)
    end)
  end

  defp csrf_token(html) do
    [_, token] = Regex.run(~r/<meta name="csrf-token" content="([^"]+)"/, html)
    token
  end

  defp create_extra_card! do
    {:ok, card} =
      Cornucopia.create_card(%{
        category: "Other",
        value: "A",
        description: "Unauthorized card",
        misc: "integration",
        edition: "webapp",
        external_id: "UNAUTHORIZED_INTEGRATION",
        language: "en",
        version: "3.0",
        owasp_scp: [],
        owasp_devguide: [],
        owasp_asvs: [],
        owasp_appsensor: [],
        capec: [],
        safecode: [],
        owasp_mastg: [],
        owasp_masvs: []
      })

    card
  end
end
