defmodule CopiWeb.ResourcesLive.Index do
  use CopiWeb, :live_view

  use Phoenix.Component

  import CopiWeb.LiveHelpers

  alias Copi.Cornucopia
  alias Copi.Cornucopia.Game

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end
end
