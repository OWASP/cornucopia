defmodule CopiWeb.UserSocket do
  use Phoenix.Socket
  require Logger

  alias Copi.RateLimiter

  ## Channels
  # channel "room:*", CopiWeb.RoomChannel

  # Socket params are passed from the client and can
  # be used to verify and authenticate a user. After
  # verification, you can put default assigns into
  # the socket that will be set for all channels, ie
  #
  #     {:ok, assign(socket, :user_id, verified_user_id)}
  #
  # To deny connection, return `:error`.
  #
  # See `Phoenix.Token` documentation for examples in
  # performing token verification on connect.
  @impl true
  def connect(_params, socket, connect_info) do
    # Extract IP address for rate limiting
    Logger.debug("WebSocket connection attempt")

    # We enforce connection rate limits at HTTP request time via
    # `CopiWeb.Plugs.RateLimiterPlug` (runs in the :browser pipeline) because
    # the HTTP `conn` reliably contains X-Forwarded-For. WebSocket
    # connect_info often doesn't include header values (only names), so
    # re-checking rate limits here can be unreliable and may see the
    # transport peer address instead. Rely on the HTTP plug instead.
  ip = get_ip_from_connect_info(connect_info)
  Logger.info("Chose IP from connect_info (no rate-check here)")

    {:ok, put_in(socket.private[:connect_info], connect_info)}
  end

  # Socket id's are topics that allow you to identify all sockets for a given user:
  #
  #     def id(socket), do: "user_socket:#{socket.assigns.user_id}"
  #
  # Would allow you to broadcast a "disconnect" event and terminate
  # all active sockets and channels for a given user:
  #
  #     CopiWeb.Endpoint.broadcast("user_socket:#{user.id}", "disconnect", %{})
  #
  # Returning `nil` makes this socket anonymous.
  @impl true
  def id(_socket), do: nil

  # Private helper to extract IP from connect_info
  defp get_ip_from_connect_info(connect_info) do
    # Prefer forwarded headers (x_headers/req_headers) if present, else peer_data
    case Copi.IPHelper.get_ip_from_connect_info(connect_info) do
      nil ->
        case connect_info[:peer_data] do
          %{address: ip} when is_tuple(ip) -> ip
          _ -> {0, 0, 0, 0}
        end
      ip -> ip
    end
  end
end
