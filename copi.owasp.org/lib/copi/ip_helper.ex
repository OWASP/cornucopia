defmodule Copi.IPHelper do
  @moduledoc """
  Helper module for extracting IP addresses from Phoenix connections and sockets.

  This module provides DRY (Don't Repeat Yourself) functionality for IP extraction
  across different parts of the application (LiveView, controllers, channels).
  """

  @doc """
  Extracts the IP address from a Phoenix.Socket.

  Returns the IP as a tuple (e.g., {127, 0, 0, 1}) or a fallback IP if not found.

  ## Examples
      iex> get_ip_from_socket(socket)
      {127, 0, 0, 1}
  """
  def get_ip_from_socket(%Phoenix.LiveView.Socket{} = socket) do
    case get_connect_info_ip(socket) do
      nil -> {127, 0, 0, 1}  # Fallback to localhost (for tests)
      ip when is_tuple(ip) -> ip
      ip -> ip
    end
  end

  def get_ip_from_socket(%Phoenix.Socket{} = socket) do
    case get_transport_ip(socket) do
      nil -> {127, 0, 0, 1}  # Fallback to localhost (for tests)
      ip when is_tuple(ip) -> ip
      ip -> ip
    end
  end

  @doc """
  Extracts the IP address from a Plug.Conn (used in controllers and plugs).

  Supports X-Forwarded-For header when behind reverse proxies.
  Returns the IP as a tuple (e.g., {127, 0, 0, 1}) or a fallback IP if not found.

  ## Examples
      iex> get_ip_from_conn(conn)
      {127, 0, 0, 1}
  """
  def get_ip_from_conn(%Plug.Conn{} = conn) do
    # Try to get real IP from X-Forwarded-For header first (for proxy scenarios)
    case get_forwarded_ip(conn) do
      nil ->
        # Fall back to remote_ip
        case conn.remote_ip do
          nil -> {127, 0, 0, 1}  # Fallback to localhost (for tests)
          ip when is_tuple(ip) -> ip
          ip -> ip
        end
      ip -> ip
    end
  end

  @doc """
  Converts an IP tuple to a string representation.

  ## Examples
      iex> ip_to_string({127, 0, 0, 1})
      "127.0.0.1"

      iex> ip_to_string({0, 0, 0, 0, 0, 0, 0, 1})
      "::1"
  """
  def ip_to_string(ip) when is_tuple(ip) do
    case :inet.ntoa(ip) do
      {:error, _} -> inspect(ip)
      ip_charlist -> to_string(ip_charlist)
    end
  end

  def ip_to_string(ip) when is_binary(ip), do: ip
  def ip_to_string(ip), do: inspect(ip)

  # Private helpers

  defp get_forwarded_ip(conn) do
    # Get X-Forwarded-For header (rightmost IP is most recent proxy, leftmost is original client)
    case Plug.Conn.get_req_header(conn, "x-forwarded-for") do
      [] -> nil
      [forwarded | _] ->
        # Take the first (leftmost) IP from the comma-separated list
        forwarded
        |> String.split(",")
        |> List.first()
        |> String.trim()
        |> parse_ip_string()
      _ -> nil
    end
  end

  defp parse_ip_string(ip_string) do
    case :inet.parse_address(String.to_charlist(ip_string)) do
      {:ok, ip_tuple} -> ip_tuple
      {:error, _} -> nil
    end
  end

  defp get_connect_info_ip(socket) do
    # Access peer_data from connect_info using nil-safe get_in
    # This prevents crashes when connect_info is nil (e.g., in tests)
    case get_in(socket.private, [:connect_info, :peer_data]) do
      %{address: address} -> address
      _ -> nil
    end
  end

  defp get_transport_ip(socket) do
    if Map.has_key?(socket, :transport_pid) && socket.transport_pid do
      # Try to get from endpoint
      case Process.info(socket.transport_pid, :dictionary) do
        {:dictionary, dict} ->
          Keyword.get(dict, :peer)
          |> case do
            {ip, _port} -> ip
            _ -> nil
          end

        _ ->
          nil
      end
    else
      nil
    end
  end
end
