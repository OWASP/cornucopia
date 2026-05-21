defmodule CopiWeb.PlayerLive.Index do
  use CopiWeb, :live_view

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game
  alias Copi.Cornucopia.Player
  alias CopiWeb.Resilience

  require Logger

  @impl true
  def mount(%{"game_id" => game_id}, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    socket = assign(socket, :client_ip, ip)

    case game_module().find(game_id) do
      {:ok, game} ->
        if game.started_at do
          {:ok,
           socket
           |> put_flash(:error, "This game has already started. New players cannot join a game in progress.")
           |> redirect(to: ~p"/games")}
        else
          {:ok,
           socket
           |> assign(:game, game)
           |> assign(:players, list_players(game_id))
           |> assign(:game_load_retry_count, 0)}
        end

      {:error, :not_found} ->
        {:ok,
         socket
         |> put_flash(:error, "Game not found.")
         |> redirect(to: ~p"/games")}

      {:error, reason} ->
        Logger.warning("Transient game load failure in PlayerLive.Index mount for game_id=#{game_id}, reason=#{inspect(reason)}")

        {:ok,
         socket
         |> put_flash(:error, "Temporary issue loading game. Please try again.")
         |> redirect(to: ~p"/games")}
    end
  end

  @impl true
  def handle_params(%{"game_id" => game_id} = params, _url, socket) do
    case game_module().find(game_id) do
      {:ok, game} ->
        # V2.2: Also check in handle_params for LiveView navigation scenarios
        if game.started_at do
          {:noreply,
           socket
           |> put_flash(:error, "This game has already started. New players cannot join a game in progress.")
           |> redirect(to: ~p"/games")}
        else
          # Assign freshly loaded game and players for LiveView client-side navigations
          players = list_players(game_id)

          {:noreply,
           socket
           |> assign(:game, game)
           |> assign(:players, players)
           |> assign(:game_load_retry_count, 0)
           |> apply_action(socket.assigns.live_action, params)}
        end

      {:error, :not_found} ->
        {:noreply,
         socket
         |> put_flash(:error, "Game not found.")
         |> redirect(to: ~p"/games")}

      {:error, reason} ->
        retry_count = socket.assigns[:game_load_retry_count] || 0

        Logger.warning(
          "Transient game load failure in PlayerLive.Index handle_params for game_id=#{game_id}, retry=#{retry_count}, reason=#{inspect(reason)}"
        )

        cond do
          socket.assigns[:game] && retry_count < Resilience.max_game_load_retries() ->
            Process.send_after(self(), {:retry_player_index_load, params}, Resilience.retry_delay_ms())

            {:noreply,
             socket
             |> assign(:game_load_retry_count, retry_count + 1)
             |> put_flash(:error, "Temporary issue loading game. Retrying...")}

          socket.assigns[:game] ->
            {:noreply,
             socket
             |> assign(:game_load_retry_count, 0)
             |> put_flash(:error, "Temporary issue loading game. Please try again.")}

          true ->
            {:noreply,
             socket
             |> put_flash(:error, "Temporary issue loading game. Please try again.")
             |> redirect(to: ~p"/games")}
        end
    end
  end

  @impl true
  def handle_info({:retry_player_index_load, params}, socket) do
    handle_params(params, nil, socket)
  end

  defp apply_action(socket, :edit, %{"id" => id}) do
    socket
    |> assign(:page_title, "Edit Player")
    |> assign(:player, Cornucopia.get_player!(id))
  end

  defp apply_action(socket, :new, %{"game_id" => game_id}) do
    game = socket.assigns.game
    socket
    |> assign(:page_title, "You're joining the game: #{game.name}")
    |> assign(:player, %Player{game_id: game_id})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Players")
    |> assign(:player, nil)
  end

  defp list_players(game_id) do
    Cornucopia.list_players(game_id)
  end

  defp game_module do
    Application.get_env(:copi, :player_live_index_game_module, Game) || Game
  end
end
