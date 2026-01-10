defmodule CopiWeb.Helpers.IPHelper do
  @moduledoc """
  Helper functions for extracting and formatting IP addresses from socket connections.
  """

  @doc """
  Extracts the IP address from a LiveView socket connection.
  
  Returns a string representation of the IP address (IPv4 or IPv6).
  Raises an error if the IP address cannot be determined, as this should never
  happen in a properly configured backend environment.
  
  ## Examples
  
      iex> get_connect_ip(socket)
      "192.168.1.1"
      
      iex> get_connect_ip(socket)
      "2001:db8::1"
  """
  def get_connect_ip(socket) do
    case Phoenix.LiveView.get_connect_info(socket, :peer_data) do
      %{address: address} when is_tuple(address) ->
        # Use Erlang's :inet.ntoa for proper IPv4/IPv6 formatting
        address
        |> :inet.ntoa()
        |> to_string()
        
      nil ->
        raise "Unable to determine IP address from socket connection. peer_data is nil. " <>
              "Ensure endpoint.ex has :peer_data in connect_info list."
        
      other ->
        raise "Unexpected peer_data format: #{inspect(other)}"
    end
  end
end
