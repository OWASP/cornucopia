defmodule CopiWeb.CoreComponents.TableComponents do
  use Phoenix.Component

  import CopiWeb.CoreComponents
  alias Phoenix.LiveView.JS
  import CopiWeb.Gettext



  attr :player, :map
  attr :player_card, :map
  attr :is_current_player, :boolean, default: false
  slot :inner_block, required: true

  def card_drop_zone(assigns) do
    ~H"""
    <div class="h-80 w-56 bg-zinc-100 rounded-lg flex justify-center items-center">
      <%= if @player_card == nil do %>
        <%= if @is_current_player do %>
          <p class="text-center">Drop a card from your hand here to play it</p>
        <% else %>
          <p class="text-center">Waiting for <%= @player.name %> to play their card</p>
        <% end %>
        <% else %>
          <%= render_slot(@inner_block) %>
      <% end %>
    </div>
    """
  end

  attr :player_card, :map
  attr :game, :map
  def vote_card(assigns) do
    ~H"""
    <%= if @player_card != nil do %>
    <div class="my-2 flex flex-row justify-start items-center">
        <.icon name="hero-hand-thumb-up" class="h-8 w-8" />
        <p class="badge ml-4"><%= Enum.count(@player_card.votes) %> / <%= Enum.count(@game.players) - 1 %></p>
    </div>
    <% end %>
    """
  end

end
