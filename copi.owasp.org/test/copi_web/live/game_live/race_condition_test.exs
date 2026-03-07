defmodule CopiWeb.GameLive.RaceConditionTest do
  use CopiWeb.ConnCase, async: false
  
  import Phoenix.LiveViewTest
  alias Copi.Cornucopia

  @game_attrs %{name: "Race Condition Test Game", edition: "webapp", suits: ["hearts", "clubs"]}

  defp create_game(_) do
    {:ok, game} = Cornucopia.create_game(@game_attrs)
    %{game: game}
  end

  defp create_players(game, count) do
    Enum.map(1..count, fn i ->
      {:ok, player} = Cornucopia.create_player(%{name: "Player #{i}", game_id: game.id})
      player
    end)
  end

  describe "Race Condition Prevention" do
    setup [:create_game]

    test "prevents duplicate card dealing with concurrent start_game requests", %{conn: conn, game: game} do
      # Create 3 players
      players = create_players(game, 3)
      
      # Verify initial state
      {:ok, initial_game} = Cornucopia.Game.find(game.id)
      assert initial_game.started_at == nil
      assert Enum.empty?(initial_game.players |> hd |> Map.get(:dealt_cards, []))

      # Simulate concurrent requests using Task.async_stream
      tasks = [
        Task.async(fn ->
          # Simulate browser 1
          {:ok, view, _html} = live(conn, "/games/#{game.id}")
          render_click(view, "start_game", %{})
        end),
        Task.async(fn ->
          # Simulate browser 2 (slight delay to simulate real race condition)
          :timer.sleep(10)
          {:ok, view, _html} = live(conn, "/games/#{game.id}")
          render_click(view, "start_game", %{})
        end),
        Task.async(fn ->
          # Simulate browser 3 (more delay)
          :timer.sleep(20)
          {:ok, view, _html} = live(conn, "/games/#{game.id}")
          render_click(view, "start_game", %{})
        end)
      ]

      # Wait for all tasks to complete
      results = Enum.map(tasks, &Task.await/1)

      # Verify final game state
      {:ok, final_game} = Cornucopia.Game.find(game.id)
      assert final_game.started_at != nil

      # Count total dealt cards across all players
      total_cards = Enum.reduce(final_game.players, 0, fn player, acc ->
        acc + length(player.dealt_cards)
      end)

      # Verify no duplicates: should be exactly 78 cards (standard deck size for webapp edition)
      assert total_cards == 78, "Expected 78 total cards, got #{total_cards}. Race condition not fixed!"

      # Verify each player has the expected number of cards (78 / 3 = 26 each, with remainder)
      expected_cards_per_player = div(78, 3)
      Enum.each(final_game.players, fn player ->
        assert length(player.dealt_cards) in [expected_cards_per_player, expected_cards_per_player + 1],
               "Player has unexpected number of cards: #{length(player.dealt_cards)}"
      end)

      # Verify no duplicate card_id across any player
      all_card_ids = Enum.flat_map(final_game.players, fn player ->
        Enum.map(player.dealt_cards, & &1.card_id)
      end)
      
      unique_card_ids = Enum.uniq(all_card_ids)
      assert length(all_card_ids) == length(unique_card_ids),
             "Found duplicate card IDs! Race condition still exists."
    end

    test "handles concurrent requests gracefully when game already started", %{conn: conn, game: game} do
      # Create 3 players
      create_players(game, 3)

      # Start the game first manually (simulating another process started it)
      {:ok, started_game} = Cornucopia.update_game(game, %{started_at: DateTime.truncate(DateTime.utc_now(), :second)})
      original_start_time = started_game.started_at

      # Simulate multiple concurrent attempts to start the same game
      tasks = Enum.map(1..3, fn i ->
        Task.async(fn ->
          delay = :rand.uniform(50)  # Random delay 0-50ms
          :timer.sleep(delay)
          
          try do
            {:ok, view, _html} = live(conn, "/games/#{game.id}")
            result = render_click(view, "start_game", %{})
            {:success, i, result}
          rescue
            e -> {:error, i, e}
          end
        end)
      end)

      # Wait for all tasks and verify they all handle the already started state gracefully
      results = Enum.map(tasks, &Task.await/1)
      
      # All should succeed but not change the game state
      assert length(results) == 3
      
      # Verify game state hasn't changed
      {:ok, final_game} = Cornucopia.Game.find(game.id)
      assert DateTime.compare(final_game.started_at, original_start_time) == :eq
      
      # Verify no additional cards were dealt
      total_cards = Enum.reduce(final_game.players, 0, fn player, acc ->
        acc + length(player.dealt_cards)
      end)
      assert total_cards == 0, "No cards should be dealt when game was already started"
    end

    test "atomic transaction works correctly under database load", %{conn: conn, game: game} do
      # Create 3 players
      create_players(game, 3)

      # Simulate high concurrency scenario
      concurrent_requests = 10
      tasks = Enum.map(1..concurrent_requests, fn i ->
        Task.async(fn ->
          delay = :rand.uniform(100)  # Random delay 0-100ms
          :timer.sleep(delay)
          
          try do
            {:ok, view, _html} = live(conn, "/games/#{game.id}")
            render_click(view, "start_game", %{})
            {:success, i}
          rescue
            e -> {:error, i, e}
          end
        end)
      end)

      # Collect results
      results = Enum.map(tasks, &Task.await/1)
      
      # Count successful vs failed attempts
      {successes, failures} = Enum.split_with(results, fn
        {:success, _} -> true
        _ -> false
      end)

      # Verify exactly one success (the one that won the race)
      assert length(successes) == 1, "Expected exactly 1 successful start, got #{length(successes)}"
      
      # Verify final game state
      {:ok, final_game} = Cornucopia.Game.find(game.id)
      assert final_game.started_at != nil
      
      # Verify no duplicate cards
      total_cards = Enum.reduce(final_game.players, 0, fn player, acc ->
        acc + length(player.dealt_cards)
      end)
      assert total_cards == 78, "Expected 78 cards, got #{total_cards}"
    end
  end
end
