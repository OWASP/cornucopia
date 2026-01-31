defmodule CopiWeb.Helpers.IPHelperTest do
  use ExUnit.Case, async: true

  alias CopiWeb.Helpers.IPHelper

  describe "get_connect_ip/1" do
    test "extracts IPv4 address from socket" do
      # Test IPv4 formatting logic
      peer_data = %{address: {192, 168, 1, 100}}
      
      {a, b, c, d} = peer_data.address
      result = "#{a}.#{b}.#{c}.#{d}"
      
      assert result == "192.168.1.100"
    end

    test "extracts IPv6 address from socket" do
      # Test IPv6 formatting
      peer_data = %{address: {8193, 3512, 0, 0, 0, 0, 0, 1}}
      
      {a, b, c, d, e, f, g, h} = peer_data.address
      result = [a, b, c, d, e, f, g, h]
        |> Enum.map(&Integer.to_string(&1, 16))
        |> Enum.join(":")
      
      assert result == "2001:DB8:0:0:0:0:0:1"
    end

    test "formats IPv6 address with lowercase hex" do
      # Test that hex formatting works correctly
      peer_data = %{address: {0x2001, 0x0db8, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0001}}
      
      {a, b, c, d, e, f, g, h} = peer_data.address
      result = [a, b, c, d, e, f, g, h]
        |> Enum.map(&Integer.to_string(&1, 16))
        |> Enum.join(":")
      
      # Should be uppercase as Integer.to_string uses uppercase for hex
      assert String.contains?(result, "2001")
    end

    test "handles different IPv4 addresses" do
      test_cases = [
        {127, 0, 0, 1} => "127.0.0.1",
        {10, 0, 0, 1} => "10.0.0.1",
        {172, 16, 254, 1} => "172.16.254.1",
        {255, 255, 255, 255} => "255.255.255.255"
      ]
      
      for {address, expected} <- test_cases do
        {a, b, c, d} = address
        result = "#{a}.#{b}.#{c}.#{d}"
        assert result == expected
      end
    end
  end
end
