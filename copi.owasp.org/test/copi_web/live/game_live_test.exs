defmodule CopiWeb.GameLiveTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest

  alias Copi.Cornucopia

  @create_attrs %{ name: "some name", edition: "webapp"}
  @update_attrs %{ name: "some updated name", edition: "webapp"}
  @invalid_attrs %{name: nil, edition: "webapp"}

  defp fixture(:game) do
    {:ok, game} = Cornucopia.create_game(@create_attrs)
    game
  end

  defp create_game(_) do
    game = fixture(:game)
    %{game: game}
  end

  describe "Index" do
    setup [:create_game]

    test "List the new game", %{conn: conn, game: game} do
      {:ok, _index_game, html} = live(conn, "/games/#{game.id}")

      assert html =~ "some name"
    end

    test "saves new game", %{conn: conn} do
      {:ok, index_live, _html} = live(conn, "/games")
      {:ok, new_conn} = index_live |> element(~s{[href="/games/new"]}) |> render_click() |> follow_redirect(conn)
      assert_redirect(index_live, Routes.game_index_path(conn, :new))


      {:ok, games_new, _html_games_new} = live(new_conn, "/games/new")

      assert _html_games_new =~ "Start A Game"

      assert games_new
             |> form("#game-form", game: @invalid_attrs)
             |> render_change() =~ "No really, give your game session a name"

      {:ok, _, html} =
        games_new
        |> form("#game-form", game: @create_attrs)
        |> render_submit()
        |> follow_redirect(conn)

      assert html =~ "Game created successfully"
      assert html =~ "some name"
    end
  end

  describe "Show" do
    setup [:create_game]

    test "displays game", %{conn: conn, game: game} do
      {:ok, _show_live, html} = live(conn, Routes.game_show_path(conn, :show, game))

      assert html =~ "Waiting for players to join the game..."
      assert html =~ game.name
    end
  end
end
