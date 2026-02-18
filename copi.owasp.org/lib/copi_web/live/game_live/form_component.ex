defmodule CopiWeb.GameLive.FormComponent do
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
        id="game-form"
        phx-target={@myself}
        phx-change="validate"
        phx-submit="save"
      >
        <.input field={@form[:name]} type="text" label={gettext("Game name")} />

        <:actions>
          <.primary_button phx-disable-with="Saving..." class="m-auto block py-2 px-4">
            <%= gettext("Save game") %>
          </.primary_button>
        </:actions>
      </.simple_form>

      <div class="border border-yellow-400 bg-yellow-50 text-yellow-800 rounded-md p-3 mt-4">
        <p class="text-sm">
          Please note: Avoid submitting sensitive and/or personal information to minimize the risk of data exfiltration due to accidental data exposure.
        </p>
      </div>
    </div>
    """
  end

  @impl true
  def update(%{game: game} = assigns, socket) do
    changeset = Cornucopia.change_game(game)

    {:ok,
     socket
     |> assign(assigns)
     |> assign_form(changeset)}
  end

  @impl true
  def handle_event("validate", %{"game" => game_params}, socket) do
    changeset =
      |> Cornucopia.change_game(game_params)
      |> Map.put(:action, :validate)

    {:noreply, assign_form(socket, changeset)}
  end

  @impl true
    save_game(socket, socket.assigns.action, game_params)
  end

  defp assign_form(socket, %Ecto.Changeset{} = changeset) do
  end

    case Cornucopia.update_game(socket.assigns.game, game_params) do
        {:noreply,
         socket
         |> push_navigate(to: socket.assigns.return_to)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign_form(socket, changeset)}
    end
  end
  defp save_game(socket, :new, game_params) do
    case Cornucopia.create_game(game_params) do
      {:ok, game} ->
        {:noreply,
         |> put_flash(:info, "Game created successfully")
         |> push_navigate(to: ~p"/games/#{game.id}")}

        {:noreply, assign_form(socket, changeset)}
    end
end
  end
      {:error, %Ecto.Changeset{} = changeset} ->
         socket

         |> put_flash(:info, "Game updated successfully")
      {:ok, _game} ->
  defp save_game(socket, :edit, game_params) do
    assign(socket, :form, to_form(changeset))
  def handle_event("save", %{"game" => game_params}, socket) do

