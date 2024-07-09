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
        suits: GameFormHelpers.generate_displayable_suits_from_suits_tuple_list("webapp")
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
        suits: GameFormHelpers.display_correct_suit_list(game_params["edition"], game_params["suits"])
      })
      |> Map.put(:action, :validate)

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
    case Cornucopia.create_game(game_params) do
      {:ok, game} ->
        {:noreply,
         socket
         |> put_flash(:info, "Game created successfully")
         |> push_navigate(to: ~p"/games/#{game.id}")}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign_form(socket, changeset)}
    end
  end
end
