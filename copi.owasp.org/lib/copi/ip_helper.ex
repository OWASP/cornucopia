defmodule Copi.IPHelper do
  @moduledoc """
  Helper module for extracting IP addresses from Phoenix connections and sockets.

  This module provides DRY (Don't Repeat Yourself) functionality for IP extraction
  across different parts of the application (LiveView, controllers, channels).
  """

  @doc """
  Extracts the IP address from a Phoenix.Socket.

  Returns the IP as a tuple (e.g., {127, 0, 0, 1}) or raises an error if not found.

  ## Examples
      iex> get_ip_from_socket(socket)
      {127, 0, 0, 1}
  """
  def get_ip_from_socket(%Phoenix.LiveView.Socket{} = socket) do
    case get_connect_info_ip(socket) do
      nil -> raise "Unable to determine IP address from socket"
      ip when is_tuple(ip) -> ip
      ip -> ip
    end
  end

  def get_ip_from_socket(%Phoenix.Socket{} = socket) do
    case get_transport_ip(socket) do
      nil -> raise "Unable to determine IP address from socket"
      ip when is_tuple(ip) -> ip
      ip -> ip
    end
  end

  @doc """
  Extracts the IP address from a Plug.Conn (used in controllers and plugs).

  Returns the IP as a tuple (e.g., {127, 0, 0, 1}) or raises an error if not found.

  ## Examples
      iex> get_ip_from_conn(conn)
      {127, 0, 0, 1}
  """
  def get_ip_from_conn(%Plug.Conn{} = conn) do
    case conn.remote_ip do
      nil -> raise "Unable to determine IP address from connection"
      ip when is_tuple(ip) -> ip
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

  defp get_connect_info_ip(socket) do
    if Map.has_key?(socket.private, :connect_info) do
      socket.private.connect_info[:peer_data][:address]
    else
      nil
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
