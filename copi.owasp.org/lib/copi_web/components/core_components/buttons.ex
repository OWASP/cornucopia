defmodule CopiWeb.CoreComponents.Buttons do

  use Phoenix.Component



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
        "phx-submit-loading:opacity-75 rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50",
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
  attr :disabled, :boolean, default: false

  slot :inner_block, required: true

  def primary_button(assigns) do
    ~H"""
    <button
      type={@type}
      class={[
        "phx-submit-loading:opacity-75 rounded-md bg-indigo-600 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600",
        @disabled && "bg-zinc-400",
        @class
      ]}
      {@rest}
    >
      <%= render_slot(@inner_block) %>
    </button>
    """
  end

  def copy_url_button(assigns) do
    ~H"""
    <div id="copy-url-container" phx-hook="CopyUrl">
      <button
        id="copy-url-btn"
        class="mt-2 rounded-md px-4 py-4 text-sm font-semibold shadow-sm transition-colors bg-gray-100 text-gray-800 hover:bg-gray-300 active:bg-gray-100 active:opacity-50"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 010 5.656l-3.535 3.535a4 4 0 01-5.656-5.656l1.414-1.414M10.172 13.828a4 4 0 010-5.656l3.535-3.535a4 4 0 015.656 5.656l-1.414 1.414" />
        </svg>
      </button>
      <input id="copied-url" class="mt-2 rounded-md px-3 py-3 text-sm font-semibold shadow-sm text-gray-500" value={@uri} />
      <span id="url-copied" class="hidden">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </span>
    </div>
    """
  end
end
