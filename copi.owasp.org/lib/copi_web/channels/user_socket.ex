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
    ip = get_ip_from_connect_info(connect_info)

    case RateLimiter.check_rate(ip, :connection) do
      {:ok, _remaining} ->
        {:ok, socket}

      {:error, :rate_limit_exceeded} ->
        Logger.warning("WebSocket connection rate limit exceeded for IP: #{inspect(ip)}")
        :error
    end
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
    case connect_info[:peer_data] do
      %{address: ip} when is_tuple(ip) -> ip
      _ -> {0, 0, 0, 0}  # Fallback IP if not available
    end
  end
end
