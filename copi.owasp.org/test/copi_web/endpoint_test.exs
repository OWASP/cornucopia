defmodule CopiWeb.EndpointTest do
  use ExUnit.Case, async: true

  test "endpoint configuration includes peer_data for LiveView socket" do
    # Get the endpoint configuration
    config = CopiWeb.Endpoint.__sockets__()
    
    # Find the /live socket configuration
    live_socket = Enum.find(config, fn {path, _} -> path == "/live" end)
    
    assert live_socket != nil, "LiveView socket should be configured"
    
    {_path, {_module, opts}} = live_socket
    
    # Check that websocket config includes peer_data
    websocket_config = Keyword.get(opts, :websocket, [])
    connect_info = Keyword.get(websocket_config, :connect_info, [])
    
    assert :peer_data in connect_info, "WebSocket should include peer_data in connect_info"
    
    # Check that longpoll config also includes peer_data
    longpoll_config = Keyword.get(opts, :longpoll, [])
    longpoll_connect_info = Keyword.get(longpoll_config, :connect_info, [])
    
    assert :peer_data in longpoll_connect_info, "Longpoll should include peer_data in connect_info"
  end

  test "endpoint is started and running" do
    assert Process.whereis(CopiWeb.Endpoint) != nil
  end
end
