defmodule CopiWeb.GameLive.Index do
  use CopiWeb, :live_view
  use Phoenix.Component

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, session, socket) do
    # V15.3.5: Use only existing, trusted IP values from assigns or session
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip")
    {:ok, assign(assign(socket, :client_ip, ip), :games, nil)}
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
    case Ecto.ULID.cast(id) do
      {:ok, game_id} ->
        case Game.find(game_id) do
          {:ok, %Game{} = game} ->
            case Cornucopia.delete_game(game) do
              {:ok, _deleted_game} ->
                {:noreply,
                 socket
                 |> put_flash(:info, "Game deleted successfully.")
                 |> assign(:games, nil)}

              {:error, _changeset} ->
                # V16.5: Fail securely with a generic user-facing error and keep state consistent.
                {:noreply, put_flash(socket, :error, "Unable to delete game.")}
            end

          {:error, _reason} ->
            # V16.5: Handle invalid/missing IDs safely without raising.
            {:noreply, put_flash(socket, :error, "Game not found.")}
        end

      :error ->
        {:noreply, put_flash(socket, :error, "Game not found.")}
    end
  end

  @impl true
  def handle_info({:update_parent, new_state}, socket) do
    {:noreply, assign(socket, :games, new_state)}
  end
end
