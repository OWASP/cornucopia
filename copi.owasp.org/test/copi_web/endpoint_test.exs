defmodule CopiWeb.EndpointTest do
  use ExUnit.Case, async: true

  test "endpoint configuration includes connect_info for LiveView socket" do
    # Get the endpoint configuration
    config = CopiWeb.Endpoint.__sockets__()
    
    # Find the /live socket configuration
    live_socket = Enum.find(config, fn 
      {path, _, _} -> path == "/live"
      _ -> false
    end)
    
    assert live_socket != nil, "LiveView socket should be configured"
    
    {_path, _module, opts} = live_socket
    
    # Check that websocket config includes connect_info
    websocket_config = Keyword.get(opts, :websocket, [])
    connect_info = Keyword.get(websocket_config, :connect_info, [])
    
    # Verify connect_info is configured (it should have session and x_headers)
    assert is_list(connect_info), "WebSocket should have connect_info configured"
    assert length(connect_info) > 0, "WebSocket connect_info should not be empty"
  end

  test "endpoint is started and running" do
    assert Process.whereis(CopiWeb.Endpoint) != nil
  end
end
