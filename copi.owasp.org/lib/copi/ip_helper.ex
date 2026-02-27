defmodule Copi.IPHelper do
  @moduledoc """
  Helper module for extracting IP addresses from Phoenix connections and sockets.

  This module provides DRY (Don't Repeat Yourself) functionality for IP extraction
  across different parts of the application (LiveView, controllers, channels).
  """
  require Logger
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
  Get the client's IP and its source from a Plug.Conn.

  Returns a tuple describing whether the IP came from a forwarded header
  or from the transport (remote_ip):

    - {:forwarded, ip_tuple}
    - {:remote, ip_tuple}
    - {:none, nil}
  """
  def get_ip_source(%Plug.Conn{} = conn) do
    case get_forwarded_ip(conn) do
      nil ->
        case conn.remote_ip do
          nil -> {:none, nil}
          ip when is_tuple(ip) -> {:remote, ip}
          ip -> {:remote, ip}
        end
      ip -> {:forwarded, ip}
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

  defp extract_first_ip(forwarded) when is_binary(forwarded) do
    forwarded
    |> String.split(",")
    |> List.first()
    |> String.trim()
    |> parse_ip_string()
  end

  defp get_forwarded_from_req_headers(headers) when is_list(headers) do
    Enum.find_value(headers, fn
      {k, v} when is_binary(k) ->
        case String.downcase(k) do
          "x-forwarded-for" -> extract_first_ip(v)
          _ -> nil
        end
      _ -> nil
    end)
  end

  defp get_forwarded_from_x_headers(x_headers) do
    cond do
      is_map(x_headers) ->
        case Map.get(x_headers, "x-forwarded-for") || Map.get(x_headers, :"x-forwarded-for") do
          nil -> nil
          v -> extract_first_ip(v)
        end

      is_list(x_headers) ->
        Enum.find_value(x_headers, fn
          {k, v} when is_binary(k) ->
            case String.downcase(k) do
              "x-forwarded-for" -> extract_first_ip(v)
              _ -> nil
            end
          v when is_binary(v) -> extract_first_ip(v)
          _ -> nil
        end)

      is_binary(x_headers) -> extract_first_ip(x_headers)
      true -> nil
    end
  end

  defp get_connect_info_ip(socket) do
    # Access peer_data from connect_info
    # This is safe in both production and test environments
    connect_info = socket.private[:connect_info]

    case connect_info do
      %Plug.Conn{} = conn ->
        # When the LiveView is mounted via the regular HTTP request,
        # connect_info can be a full Plug.Conn. First try X-Forwarded-For,
        # then peer_data, then remote_ip.
        case get_forwarded_ip(conn) do
          nil ->
            case conn.private[:peer_data] do
              %{address: address} -> address
              _ -> conn.remote_ip
            end
          ip -> ip
        end

      map when is_map(map) ->
        # connect_info may be a map for some sockets. Try to extract
        # X-Forwarded-For from common locations, then peer_data.
        forwarded =
          cond do
            headers = Map.get(map, :req_headers) -> get_forwarded_from_req_headers(headers)
            xh = Map.get(map, :x_headers) -> get_forwarded_from_x_headers(xh)
            true -> nil
          end

        case forwarded do
          nil ->
            case Map.get(map, :peer_data) do
              %{address: address} -> address
              _ -> nil
            end
          ip -> ip
        end

      _ ->
        nil
    end
  end

  @doc """
  Extract IP from a connect_info map (as passed to socket connect) or return nil.
  This is useful from channel UserSocket.connect/3 where we only have the connect_info.
  """
  def get_ip_from_connect_info(%{} = connect_info) do
    # Look in several common keys where headers may be placed by adapters
    header_candidates = [
      :x_headers,
      :req_headers,
      :headers,
      :request_headers,
      :request_header,
      :headers_in
    ]

    forwarded =
      Enum.find_value(header_candidates, fn key ->
        case Map.get(connect_info, key) do
          nil -> nil
          value ->
            case extract_first_ip_from_headers(value) do
              nil -> nil
              ip -> ip
            end
        end
      end)

    case forwarded do
      nil ->
        case Map.get(connect_info, :peer_data) do
          %{address: address} -> address
          _ -> nil
        end
      ip -> ip
    end
  end

  defp extract_first_ip_from_headers(value) do
    cond do
      is_list(value) ->
        # list of {k,v} tuples or list of strings
        Enum.find_value(value, fn
          {k, v} when is_binary(k) ->
            case String.downcase(k) do
              "x-forwarded-for" -> extract_first_ip(v)
              _ -> nil
            end
          {k, v} when is_atom(k) ->
            case Atom.to_string(k) |> String.downcase() do
              "x-forwarded-for" -> extract_first_ip(v)
              _ -> nil
            end
          v when is_binary(v) -> extract_first_ip(v)
          _ -> nil
        end)

      is_map(value) ->
        case Map.get(value, "x-forwarded-for") || Map.get(value, :"x-forwarded-for") do
          nil -> nil
          v -> extract_first_ip(v)
        end

      is_binary(value) -> extract_first_ip(value)

      true -> nil
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
