defmodule CopiWeb.CoreComponents.Buttons do
  use Phoenix.Component

  alias Phoenix.LiveView.JS
  import CopiWeb.Gettext

  @doc """
  Renders a button.

  ## Examples

      <.button>Send!</.button>
      <.button phx-click="go" class="ml-2">Send!</.button>
  """
  attr :type, :string, default: nil
  attr :class, :string, default: nil
  attr :rest, :global, include: ~w(disabled form name value)

  slot :inner_block, required: true

  def button(assigns) do
    ~H"""
    <button
      type={@type}
      class={[
        "phx-submit-loading:opacity-75 rounded-lg bg-zinc-900 hover:bg-zinc-900 py-2 px-3",
        "text-sm font-semibold leading-6 text-white active:text-white/80",
        @class
      ]}
      {@rest}
    >
      <%= render_slot(@inner_block) %>
    </button>
    """
  end

  attr :type, :string, default: nil
  attr :class, :string, default: nil
  attr :rest, :global, include: ~w(disabled form name value)

  slot :inner_block, required: true

  def primary_button(assigns) do
    ~H"""
    <button
      type={@type}
      class={[
        "phx-submit-loading:opacity-75 rounded-lg bg-zinc-900 hover:bg-zinc-900 py-2 px-3",
        "text-sm font-semibold leading-6 text-white active:text-white/80",
        @class
      ]}
      {@rest}
    >
      <%= render_slot(@inner_block) %>
    </button>
    """
  end

  # def vote() do
  #   ~H"""
  #       <%= if player_card != nil do %>
  #   <span class="vote voted mine">
  #     <img src="/images/vote.png" title="You can't vote for your own card" alt="A thumbs-up image for voting"/>
  #     <br />
  #     <span class="badge"><%= Enum.count(player_card.votes) %> / <%= Enum.count(@game.players) - 1 %></span>
  #   </span>
  #     <%= if Enum.count(player_card.votes) > (Enum.count(@game.players) - 1) / 2 do %>
  #     <br /><span class="scored">Scored!</span>
  #     <% end %>
  #   <% else %>
  #   <span class="vote none">
  #     &nbsp;
  #   </span>
  #   <% end %>
  #   """
  # end
end
