defmodule CopiWeb.PlayerLive.FormComponent do
  use CopiWeb, :live_component
  use Phoenix.Component

  alias Copi.Cornucopia

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
        <.input field={@form[:name]} type="text" label={gettext "Player Name"} />

        <.input field={@form[:game_id]} type="hidden" />

        <:actions>
          <.primary_button phx-disable-with="Joining..." class="m-auto block py-2 px-3"><%= gettext "Join the game" %></.primary_button>
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
    # Get the IP address for rate limiting
    ip_address = get_connect_ip(socket)
    
    # Check rate limit before creating player
    case Copi.RateLimiter.check_rate(ip_address, :player_creation) do
      {:ok, _remaining} ->
        case Cornucopia.create_player(player_params) do
          {:ok, player} ->
            # Record the action after successful creation
            Copi.RateLimiter.record_action(ip_address, :player_creation)

            {:ok, updated_game} = Cornucopia.Game.find(socket.assigns.player.game_id)
            CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

            {:noreply,
             socket
             |> assign(:game, updated_game)
             |> push_navigate(to: ~p"/games/#{player.game_id}/players/#{player.id}")}

          {:error, %Ecto.Changeset{} = changeset} ->
            {:noreply, assign_form(socket, changeset)}
        end
        
      {:error, :rate_limited, retry_after} ->
        {:noreply,
         socket
         |> put_flash(
           :error,
           "Rate limit exceeded. Too many players created from your IP address. " <>
           "Please try again in #{retry_after} seconds. " <>
           "This limit helps ensure service availability for all users."
         )
         |> assign_form(socket.assigns.form.source)}
    end
  end

  def topic(game_id) do
    "game:#{game_id}"
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
