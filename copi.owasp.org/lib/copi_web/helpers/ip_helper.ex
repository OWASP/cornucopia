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
      %{address: {a, b, c, d}} ->
        # IPv4 address
        "#{a}.#{b}.#{c}.#{d}"
        
      %{address: {a, b, c, d, e, f, g, h}} ->
        # IPv6 address - format as colon-separated hex
        [a, b, c, d, e, f, g, h]
        |> Enum.map(&Integer.to_string(&1, 16))
        |> Enum.join(":")
        
      nil ->
        raise "Unable to determine IP address from socket connection. peer_data is nil."
        
      other ->
        raise "Unexpected peer_data format: #{inspect(other)}"
    end
  end
end
