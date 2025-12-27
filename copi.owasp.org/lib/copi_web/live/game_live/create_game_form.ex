defmodule CopiWeb.GameLive.CreateGameForm do
  use CopiWeb, :live_component

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game
  alias CopiWeb.GameLive.GameFormHelpers, as: GameFormHelpers

  @impl true
  def render(assigns) do
    ~H"""
    <div >
      <.header1 >
        <%= @title %>
        <:subtitle>Use this form to manage game records in your database.</:subtitle>
      </.header1>

      <.simple_form
        for={@form}
        id="game-form"
        phx-target={@myself}
        phx-change="validate"
        phx-submit="save"
      >
        <.input field={@form[:name]} type="text" label={gettext "Give your game session a friendly name so people joining know what's up"} />

        <.input
          field={@form[:edition]}
          type="select"
          label={gettext "Choose the type of game you wish to play"}
          options={[
              {"Cornucopia Web (for web apps and APIs)", "webapp"},
              {"Cornucopia Mobile (for mobile apps)", "mobileapp"},
              {"Elevation of Privilege (for cloud platforms, infrastructure, apps, anything!)", "eop"},
              {"Elevation of MLSec (for machine learning)", "mlsec"},
              {"OWASP Cumulus (for DevOps and Cloud projects)", "cumulus"},
          ]}
          >
        </.input>

        <.input field={@form[:suits]} label={gettext("Select the suits you want to play:")} multiple={true}  type="checkbox" options={GameFormHelpers.get_suits_from_selected_deck(assigns)} />

        <:actions>
          <.primary_button phx-disable-with="Starting game..." class=""><%= gettext "Create the game" %></.primary_button>
        </:actions>
      </.simple_form>
    </div>
    """
  end

  def update(%{game: _} = assigns, socket) do
    changeset =
      Cornucopia.change_game(%Game{
        edition: "",
        name: "",
        suits: GameFormHelpers.generate_suit_list_formatted_for_checkbox("webapp")
      })

    {:ok,
     socket
     |> assign(assigns)
     |> assign_form(changeset)}
  end

  @impl true
  def handle_event("validate", %{"game" => game_params}, socket) do

    changeset =
      socket.assigns.game
      |> Cornucopia.change_game(%{
        edition: game_params["edition"],
        name: game_params["name"],
        suits: GameFormHelpers.display_appropriate_suits_list(game_params["edition"], game_params["suits"])
      })
      |> Map.put(:action, :validate)

    send(self(), {:update_parent, changeset})

    {:noreply, assign_form(socket, changeset)}
  end

  def handle_event("save", %{"game" => game_params}, socket) do

    game_with_suits = %{
      name: game_params["name"],
      edition: game_params["edition"],
      suits: GameFormHelpers.format_suits_before_saving_game(game_params["suits"])
    }

    save_game(socket, socket.assigns.action, game_with_suits)
  end

  defp assign_form(socket, %Ecto.Changeset{} = changeset) do
    assign(socket, :form, to_form(changeset))
  end

  defp save_game(socket, :edit, game_params) do
    case Cornucopia.update_game(socket.assigns.game, game_params) do
      {:ok, _game} ->
        {:noreply,
         socket
         |> put_flash(:info, "Game updated successfully")
         |> push_redirect(to: socket.assigns.return_to)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign_form(socket, changeset)}
    end
  end

  defp save_game(socket, :new, game_params) do
    # Get the IP address for rate limiting
    ip_address = get_connect_ip(socket)
    
    # Check rate limit before creating game
    case Copi.RateLimiter.check_rate(ip_address, :game_creation) do
      {:ok, _remaining} ->
        case Cornucopia.create_game(game_params) do
          {:ok, game} ->
            # Record the action after successful creation
            Copi.RateLimiter.record_action(ip_address, :game_creation)
            
            {:noreply,
             socket
             |> put_flash(:info, "Game created successfully")
             |> push_navigate(to: ~p"/games/#{game.id}")}

          {:error, %Ecto.Changeset{} = changeset} ->
            {:noreply, assign_form(socket, changeset)}
        end
        
      {:error, :rate_limited, retry_after} ->
        {:noreply,
         socket
         |> put_flash(
           :error,
           "Rate limit exceeded. Too many games created from your IP address. " <>
           "Please try again in #{retry_after} seconds. " <>
           "This limit helps ensure service availability for all users."
         )
         |> assign_form(socket.assigns.form.source)}
    end
  end

  defp get_connect_ip(socket) do
    case get_connect_info(socket, :peer_data) do
      %{address: {a, b, c, d}} -> "#{a}.#{b}.#{c}.#{d}"
      %{address: {a, b, c, d, e, f, g, h}} -> 
        :inet.ntoa({a, b, c, d, e, f, g, h}) |> to_string()
      _ -> "unknown"
    end
  end
end
