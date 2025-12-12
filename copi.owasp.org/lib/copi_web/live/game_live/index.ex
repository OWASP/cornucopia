defmodule CopiWeb.GameLive.Index do
  use CopiWeb, :live_view
  use Phoenix.Component

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    # Rate limit WebSocket connections
    ip_address = get_connect_ip(socket)
    
    case Copi.RateLimiter.check_rate(ip_address, :connection) do
      {:ok, _remaining} ->
        Copi.RateLimiter.record_action(ip_address, :connection)
        {:ok, assign(socket, :games, nil)}
        
      {:error, :rate_limited, retry_after} ->
        {:ok,
         socket
         |> put_flash(
           :error,
           "Connection rate limit exceeded. Too many connections from your IP address. " <>
           "Please try again in #{retry_after} seconds."
         )
         |> assign(:games, nil)}
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

  defp get_connect_ip(socket) do
    case get_connect_info(socket, :peer_data) do
      %{address: {a, b, c, d}} -> "#{a}.#{b}.#{c}.#{d}"
      %{address: {a, b, c, d, e, f, g, h}} -> 
        "#{Integer.to_string(a, 16)}:#{Integer.to_string(b, 16)}:#{Integer.to_string(c, 16)}:#{Integer.to_string(d, 16)}:#{Integer.to_string(e, 16)}:#{Integer.to_string(f, 16)}:#{Integer.to_string(g, 16)}:#{Integer.to_string(h, 16)}"
      _ -> "unknown"
    end
  end

end
