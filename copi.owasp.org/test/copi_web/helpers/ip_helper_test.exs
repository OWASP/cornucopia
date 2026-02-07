defmodule CopiWeb.Helpers.IPHelperTest do
  use CopiWeb.ConnCase
  import Phoenix.LiveViewTest
  
  alias Phoenix.LiveView.Socket

  describe "get_connect_ip/1" do
    test "extracts IPv4 address from socket" do
      socket = %Socket{
        private: %{
          connect_info: %{
            peer_data: %{address: {192, 168, 1, 100}, port: 12345, ssl_cert: nil}
          }
        }
      }
      
      assert CopiWeb.Helpers.IPHelper.get_connect_ip(socket) == "192.168.1.100"
    end

    test "extracts IPv6 address from socket" do
      socket = %Socket{
        private: %{
          connect_info: %{
            peer_data: %{address: {8193, 3512, 0, 0, 0, 0, 0, 1}, port: 12345, ssl_cert: nil}
          }
        }
      }
      
      assert CopiWeb.Helpers.IPHelper.get_connect_ip(socket) == "2001:DB8:0:0:0:0:0:1"
    end

    test "handles localhost IPv4 address" do
      socket = %Socket{
        private: %{
          connect_info: %{
            peer_data: %{address: {127, 0, 0, 1}, port: 12345, ssl_cert: nil}
          }
        }
      }
      
      assert CopiWeb.Helpers.IPHelper.get_connect_ip(socket) == "127.0.0.1"
    end

    test "handles different IPv4 addresses" do
      test_cases = [
        {{10, 0, 0, 1}, "10.0.0.1"},
        {{172, 16, 254, 1}, "172.16.254.1"}
      ]
      
      for {address, expected} <- test_cases do
        socket = %Socket{
          private: %{
            connect_info: %{
              peer_data: %{address: address, port: 12345, ssl_cert: nil}
            }
          }
        }
        
        assert CopiWeb.Helpers.IPHelper.get_connect_ip(socket) == expected
      end
    end

    test "returns fallback IP when peer_data is nil" do
      socket = %Socket{
        private: %{
          connect_info: %{peer_data: nil}
        }
      }
      
      assert CopiWeb.Helpers.IPHelper.get_connect_ip(socket) == "127.0.0.1"
    end
  end
end
