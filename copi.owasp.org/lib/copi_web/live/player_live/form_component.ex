defmodule CopiWeb.PlayerLive.FormComponent do
  use CopiWeb, :live_component
  use Phoenix.Component

  alias Copi.Cornucopia
  alias Copi.RateLimiter

  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <.header1>
        <%= @title %>
      </.header1>

      <.simple_form
        for={@form}
        id="player-form"
        phx-target={@myself}
        phx-change="validate"
        phx-submit="save"
      >
        <.input field={@form[:name]} type="text" label={gettext("Player Name")} />

        <input type="hidden" name={@form[:game_id].name} value={@form[:game_id].value} />

        <div class="border border-yellow-400 bg-yellow-50 text-yellow-800 rounded-md p-3 mt-2">
          <p class="text-sm">
            Please note: Avoid submitting sensitive and/or personal information to minimize the risk of data exfiltration due to accidental data exposure.
          </p>
          <p>
            Please read about:
          </p>
          <a href="/privacy" target="_blank" title="Privacy Notice">
            How we process your data
          </a>
        </div>

        <:actions>
          <.primary_button phx-disable-with="Joining..." class="m-auto block py-2 px-4">
            <%= gettext("Join game") %>
          </.primary_button>
        </:actions>
      </.simple_form>
    </div>
    """
  end

  @impl true
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

  @impl true
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
         |> push_navigate(to: socket.assigns.return_to)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign_form(socket, changeset)}
    end
  end

  defp save_player(socket, :new, player_params) do
    ip = socket.assigns[:client_ip] || {127, 0, 0, 1}

    case RateLimiter.check_rate(ip, :player_creation) do
      {:ok, _remaining} ->
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

      {:error, :rate_limit_exceeded} ->
        {:noreply,
         socket
         |> put_flash(:error, "Too many player creation attempts. Please try again later.")
         |> assign_form(Cornucopia.change_player(socket.assigns.player))}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
  end
end
