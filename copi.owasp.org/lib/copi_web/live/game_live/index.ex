defmodule CopiWeb.GameLive.Index do
  use CopiWeb, :live_view
  use Phoenix.Component

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      # Rate limit WebSocket connections (only on connected mount)
      ip_address = CopiWeb.Helpers.IPHelper.get_connect_ip(socket)
      Phoenix.PubSub.subscribe(Copi.PubSub, "games")

      case Copi.RateLimiter.check_and_record(ip_address, :connection) do
        {:ok, _remaining} ->
          {:ok, assign(socket, games: nil, ip_address: ip_address)}

        {:error, :rate_limited, retry_after} ->
          {:ok,
           socket
           |> put_flash(
             :error,
             "Connection rate limit exceeded. Too many connections from your IP address. " <>
             "Please try again in #{retry_after} seconds."
           )
           |> assign(games: nil, ip_address: ip_address)}
      end
    else
      # Disconnected mount (initial static render) - no WebSocket yet
      # Assign games: nil to match original behavior expected by templates
      {:ok, assign(socket, games: nil, ip_address: "127.0.0.1")}
    end
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :new, _params) do
    socket
    |> assign(:page_title, "Create a new game")
    |> assign(:game, %Game{})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Games")
    |> assign(:game, nil)
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    game = Cornucopia.get_game!(id)
    {:ok, _} = Cornucopia.delete_game(game)

    {:noreply, assign(socket, :games, list_games())}
  end

  defp list_games do
    Cornucopia.list_games()
  end

  @impl true
  def handle_info({:update_parent, new_state}, socket) do
    {:noreply, assign(socket, :games, new_state)}
  end

end
