defmodule CopiWeb.GameLive.GameFormHelpersTest do
  use Copi.DataCase, async: false
  alias CopiWeb.GameLive.GameFormHelpers

  describe "generate_suit_list_formatted_for_checkbox/1" do
    test "generates checkbox formatted suit list for webapp edition" do
      result = GameFormHelpers.generate_suit_list_formatted_for_checkbox("webapp")
      
      assert is_list(result)
      assert length(result) > 0
      # Check that all items are strings with edition prefix
      assert Enum.all?(result, fn suit -> String.starts_with?(suit, "webapp-") end)
    end

    test "generates checkbox formatted suit list for mobileapp edition" do
      result = GameFormHelpers.generate_suit_list_formatted_for_checkbox("mobileapp")
      
      assert is_list(result)
      assert Enum.all?(result, fn suit -> String.starts_with?(suit, "mobileapp-") end)
    end

    test "generates checkbox formatted suit list for eop edition" do
      result = GameFormHelpers.generate_suit_list_formatted_for_checkbox("eop")
      
      assert is_list(result)
      assert Enum.all?(result, fn suit -> String.starts_with?(suit, "eop-") end)
    end
  end

  describe "format_suits_before_saving_game/1" do
    test "removes edition prefix from suits" do
      suits = ["webapp-hearts", "webapp-diamonds", "webapp-clubs"]
      result = GameFormHelpers.format_suits_before_saving_game(suits)
      
      assert result == ["hearts", "diamonds", "clubs"]
    end

    test "filters out empty strings" do
      suits = ["webapp-hearts", "", "webapp-diamonds"]
      result = GameFormHelpers.format_suits_before_saving_game(suits)
      
      assert result == ["hearts", "diamonds"]
      refute "" in result
    end

    test "handles suits from different editions" do
      suits = ["eop-elevation", "mobileapp-data"]
      result = GameFormHelpers.format_suits_before_saving_game(suits)
      
      assert result == ["elevation", "data"]
    end

    test "handles empty list" do
      result = GameFormHelpers.format_suits_before_saving_game([])
      assert result == []
    end

    test "handles list with only empty strings" do
      result = GameFormHelpers.format_suits_before_saving_game(["", "", ""])
      assert result == []
    end
  end

  describe "format_list_of_suits_for_checkbox/1" do
    test "formats suits for webapp edition" do
      result = GameFormHelpers.format_list_of_suits_for_checkbox("webapp")
      
      assert is_list(result)
      # Check format is {key, label} tuples
      assert Enum.all?(result, fn 
        {key, label} when is_binary(key) and is_binary(label) -> true
        _ -> false
      end)
      
      # Check keys have edition prefix
      Enum.each(result, fn {key, _label} ->
        assert String.starts_with?(key, "webapp-")
      end)
    end

    test "formats suits for mobileapp edition" do
      result = GameFormHelpers.format_list_of_suits_for_checkbox("mobileapp")
      
      assert is_list(result)
      Enum.each(result, fn {key, _label} ->
        assert String.starts_with?(key, "mobileapp-")
      end)
    end

    test "capitalizes suit labels" do
      result = GameFormHelpers.format_list_of_suits_for_checkbox("webapp")
      
      # All labels should be capitalized
      Enum.each(result, fn {_key, label} ->
        assert label == String.capitalize(label)
      end)
    end
  end

  describe "display_appropriate_suits_list/2" do
    test "returns generated list when suits contains only empty string" do
      suits = [""]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)
      
      assert is_list(result)
      assert Enum.any?(result, fn suit -> String.starts_with?(suit, "webapp-") end)
      refute Enum.any?(result, fn suit -> String.starts_with?(suit, "companion-") end)
    end

    test "returns same suits when they match the edition" do
      suits = ["", "webapp-hearts", "webapp-diamonds"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)
      
      assert result == suits
    end

    test "generates new list when suits don't match edition" do
      suits = ["", "mobileapp-data", "mobileapp-security"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)
      
      # Should generate webapp suits instead
      assert is_list(result)
      assert Enum.any?(result, fn suit -> String.starts_with?(suit, "webapp-") end)
      refute Enum.any?(result, fn suit -> String.starts_with?(suit, "mobileapp-") end)
    end

    test "handles switching between editions" do
      suits = ["", "eop-elevation"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)
      
      assert Enum.any?(result, fn suit -> String.starts_with?(suit, "webapp-") end)
      refute Enum.any?(result, fn suit -> String.starts_with?(suit, "eop-") end)
    end

    test "keeps companion suits when the selected edition still matches" do
      suits = ["", "webapp-Authentication", "companion-Large Language Models"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)

      assert result == suits
    end

    test "keeps companion-only selections for host editions" do
      suits = ["", "companion-Large Language Models"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)

      assert result == suits
    end
  end

  describe "companion suit helpers" do
    test "does not include companion defaults for webapp and mobileapp" do
      webapp_suits = GameFormHelpers.generate_selected_suits_for_new_game("webapp")
      mobileapp_suits = GameFormHelpers.generate_selected_suits_for_new_game("mobileapp")

      refute Enum.any?(webapp_suits, fn suit -> String.starts_with?(suit, "companion-") end)
      refute Enum.any?(mobileapp_suits, fn suit -> String.starts_with?(suit, "companion-") end)
    end

    test "does not add companion defaults to other games" do
      result = GameFormHelpers.generate_selected_suits_for_new_game("eop")

      refute Enum.any?(result, fn suit -> String.starts_with?(suit, "companion-") end)
    end

    # Regression test for issue #2842 – single non-empty suit matching edition
    test "returns same suits when exactly one suit matches the edition" do
      suits = ["webapp-authentication"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)

      assert result == suits
    end

    # Regression test for issue #2842 – single non-empty suit NOT matching edition
    test "generates new list when exactly one suit does not match the edition" do
      suits = ["mobileapp-storage"]
      result = GameFormHelpers.display_appropriate_suits_list("webapp", suits)

      assert is_list(result)
      assert Enum.any?(result, fn suit -> String.starts_with?(suit, "webapp-") end)
      refute Enum.any?(result, fn suit -> String.starts_with?(suit, "companion-") end)
      refute Enum.any?(result, fn suit -> String.starts_with?(suit, "mobileapp-") end)
    end
  end

  describe "get_suits_from_selected_deck/1" do
    test "returns webapp suits when no changes in form" do
      assigns = %{
        form: %{
          source: %{
            changes: nil
          }
        }
      }
      
      result = GameFormHelpers.get_suits_from_selected_deck(assigns)
      
      assert is_list(result)
      Enum.each(result, fn {key, _label} ->
        assert String.starts_with?(key, "webapp-")
      end)
    end

    test "returns webapp suits when empty changes in form" do
      assigns = %{
        form: %{
          source: %{
            changes: %{}
          }
        }
      }
      
      result = GameFormHelpers.get_suits_from_selected_deck(assigns)
      
      assert is_list(result)
      Enum.each(result, fn {key, _label} ->
        assert String.starts_with?(key, "webapp-")
      end)
    end

    test "returns edition-specific suits when edition in changes" do
      assigns = %{
        form: %{
          source: %{
            changes: %{edition: "mobileapp"}
          }
        }
      }
      
      result = GameFormHelpers.get_suits_from_selected_deck(assigns)
      
      assert is_list(result)
      Enum.each(result, fn {key, _label} ->
        assert String.starts_with?(key, "mobileapp-")
      end)
    end

    test "handles eop edition in changes" do
      assigns = %{
        form: %{
          source: %{
            changes: %{edition: "eop"}
          }
        }
      }
      
      result = GameFormHelpers.get_suits_from_selected_deck(assigns)
      
      Enum.each(result, fn {key, _label} ->
        assert String.starts_with?(key, "eop-")
      end)
    end
  end
end
