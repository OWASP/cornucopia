defmodule CopiWeb.PlayerLive.FormComponent do
  use CopiWeb, :live_component

  alias Copi.Cornucopia

  @impl true
  def update(%{player: player} = assigns, socket) do
    changeset = Cornucopia.change_player(player)

    {:ok,
     socket
     |> assign(assigns)
     |> assign(:changeset, changeset)}
  end

  @impl true
  def handle_event("validate", %{"player" => player_params}, socket) do
    changeset =
      socket.assigns.player
      |> Cornucopia.change_player(player_params)
      |> Map.put(:action, :validate)

    {:noreply, assign(socket, :changeset, changeset)}
  end

  def handle_event("save", %{"player" => player_params}, socket) do
    save_player(socket, socket.assigns.action, player_params)
  end

  defp save_player(socket, :edit, player_params) do
    case Cornucopia.update_player(socket.assigns.player, player_params) do
      {:ok, _player} ->
        {:noreply,
         socket
         |> put_flash(:info, "Player updated successfully")
         |> push_redirect(to: socket.assigns.return_to)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign(socket, :changeset, changeset)}
    end
  end

  defp save_player(socket, :new, player_params) do
    case Cornucopia.create_player(player_params) do
      {:ok, player} ->
        {:ok, updated_game} = Cornucopia.Game.find(socket.assigns.player.game_id)
        CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

        {:noreply,
         socket
         |> assign(:game, updated_game)
         |> push_redirect(to: Routes.player_show_path(socket, :show, player.game_id, player))}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign(socket, changeset: changeset)}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
