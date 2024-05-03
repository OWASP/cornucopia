defmodule CopiWeb.PlayerLive.FormComponent do
  use CopiWeb, :live_component
  use Phoenix.Component

  alias Copi.Cornucopia

  @impl true

  def render(assigns) do
    ~H"""
    <div>
      <.header>
        <%= @title %>
        <:subtitle>Use this form to manage player records in your database.</:subtitle>
      </.header>

      <.simple_form
        for={@form}
        id="player-form"
        phx-target={@myself}
        phx-change="validate"
        phx-submit="save"
      >
        <.input field={@form[:name]} type="text" label={gettext "Player Name"} />

        <.input field={@form[:game_id]} type="hidden" />

        <:actions>
          <.button phx-disable-with="Joining..." class="py-2 px-3"><%= gettext "Join the game" %></.button>
        </:actions>
      </.simple_form>
    </div>
    """
  end

  def update(%{player: player} = assigns, socket) do
    changeset = Cornucopia.change_player(player)

    {:ok,
     socket
     |> assign(assigns)
     |> assign_form(changeset)}
  end

  @impl true
  def handle_event("validate", %{"player" => player_params}, socket) do
    changeset =
      socket.assigns.player
      |> Cornucopia.change_player(player_params)
      |> Map.put(:action, :validate)

      {:noreply, assign_form(socket, changeset)}
  end

  def handle_event("save", %{"player" => player_params}, socket) do
    save_player(socket, socket.assigns.action, player_params)
  end

  defp assign_form(socket, %Ecto.Changeset{} = changeset) do
    assign(socket, :form, to_form(changeset))
  end

  defp save_player(socket, :edit, player_params) do
    case Cornucopia.update_player(socket.assigns.player, player_params) do
      {:ok, _player} ->
        {:noreply,
         socket
         |> put_flash(:info, "Player updated successfully")
         |> push_redirect(to: socket.assigns.return_to)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign_form(socket, changeset)}
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
         |> push_navigate(to: ~p"/games/#{player.game_id}/players/#{player.id}")}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign_form(socket, changeset)}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
