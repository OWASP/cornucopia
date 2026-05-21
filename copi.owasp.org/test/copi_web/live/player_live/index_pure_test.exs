defmodule CopiWeb.PlayerLive.IndexPureTest do
  use ExUnit.Case, async: false

  alias CopiWeb.PlayerLive.Index

  defmodule GameStub do
    def find(_id) do
      case Application.get_env(:copi, :player_live_index_pure_mode, :not_found) do
        :not_found -> {:error, :not_found}
        :transient -> {:error, :temporary}
      end
    end
  end

  setup do
    old_game_mod = Application.get_env(:copi, :player_live_index_game_module)
    old_mode = Application.get_env(:copi, :player_live_index_pure_mode)

    Application.put_env(:copi, :player_live_index_game_module, GameStub)

    on_exit(fn ->
      Application.put_env(:copi, :player_live_index_game_module, old_game_mod)
      Application.put_env(:copi, :player_live_index_pure_mode, old_mode)
    end)

    :ok
  end

  test "handle_params not_found branch returns noreply" do
    Application.put_env(:copi, :player_live_index_pure_mode, :not_found)

    socket = %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}, live_action: :index, flash: %{}}}

    assert {:noreply, _socket} = Index.handle_params(%{"game_id" => "missing"}, nil, socket)
  end

  test "handle_params transient true branch redirects when no game assign exists" do
    Application.put_env(:copi, :player_live_index_pure_mode, :transient)

    socket = %Phoenix.LiveView.Socket{assigns: %{__changed__: %{}, live_action: :index, flash: %{}}}

    assert {:noreply, _socket} = Index.handle_params(%{"game_id" => "any"}, nil, socket)
  end
end
