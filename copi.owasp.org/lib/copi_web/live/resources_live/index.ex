defmodule CopiWeb.ResourcesLive.Index do
  use CopiWeb, :live_view

  use Phoenix.Component

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end
end
