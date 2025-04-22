defmodule CopiWeb.CoreComponents.TableComponents do
  use Phoenix.Component

  import CopiWeb.CoreComponents

  attr :player, :map
  attr :player_card, :map
  attr :is_current_player, :boolean, default: false
  attr :first_card_played, :map
  attr :highest_scoring_card, :map
  slot :inner_block, required: true

  def card_drop_zone(assigns) do
    ~H"""
    <div class="h-80 w-56 border-2 border-zinc-100 rounded-lg flex justify-center items-center">
      <%= if @player_card == nil do %>
        <%= if @is_current_player do %>
          <div class="h-5/6 w-5/6 shadow-md bg-zinc-100 border-2 border-zinc-200 rounded-lg animate-pulse flex justify-center items-center">
          <%= if @first_card_played do %>
            <p class="text-center text-zinc-600">You <em>should</em> play a <br /><%= @first_card_played.card.category %> <br /> card</p>
          <% else %>
            <p class="text-center text-zinc-600">You can play<br />any <br /> card</p>
          <% end %>
          </div>
        <% else %>
          <p class="text-center">Waiting for <%= @player.name %> to play their card</p>
        <% end %>
        <% else %>
          <div
          class={[
          "",
          @player_card && @highest_scoring_card && @player_card.id == @highest_scoring_card.id && "ring-offset-2 ring-4 ring-amber-300"
        ]}
          >
            <%= render_slot(@inner_block) %>
          </div>
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
