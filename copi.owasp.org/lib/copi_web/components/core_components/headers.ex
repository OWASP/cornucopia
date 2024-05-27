defmodule CopiWeb.CoreComponents.Headers do
  use Phoenix.Component

  alias Phoenix.LiveView.JS
  import CopiWeb.Gettext

    @doc """
  Renders a header with title.
  """
  attr :class, :string, default: nil

  slot :inner_block, required: true
  slot :subtitle
  slot :actions

  def header(assigns) do
    ~H"""
    <header class={[@actions != [] && "flex items-center justify-between gap-6", @class]}>
      <div>
        <h1 class="text-lg font-semibold leading-8 text-zinc-800">
          <%= render_slot(@inner_block) %>
        </h1>
        <p :if={@subtitle != []} class="mt-2 text-sm leading-6 text-zinc-600">
          <%= render_slot(@subtitle) %>
        </p>
      </div>
      <div class="flex-none"><%= render_slot(@actions) %></div>
    </header>
    """
  end


  @doc """
  Renders a header with title.
  """
  attr :class, :string, default: nil

  slot :inner_block, required: true
  slot :subtitle
  slot :actions

  def header1(assigns) do
    ~H"""
      <h1 class="my-4 py-4 text-4xl font-bold leading-8 text-zinc-800">
        <%= render_slot(@inner_block) %>
      </h1>
    """
  end


  attr :class, :string, default: nil

  slot :inner_block, required: true
  slot :subtitle
  slot :actions

  def header2(assigns) do
    ~H"""
      <h2 class="my-4 text-2xl font-semibold leading-8 text-zinc-800">
        <%= render_slot(@inner_block) %>
      </h2>
    """
  end
end
