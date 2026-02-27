defmodule CopiWeb.PrivacyLive.Index do
  use CopiWeb, :live_view

  use Phoenix.Component

  @impl true
  def mount(_params, session, socket) do
    ip = socket.assigns[:client_ip] || Map.get(session, "client_ip") || Copi.IPHelper.get_ip_from_socket(socket)
    {:ok, assign(socket, :client_ip, ip)}
  end
end
