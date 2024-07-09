defmodule Copi.CardsTest do
  use Copi.DataCase

  alias Copi.Cornucopia

  describe "cards" do
    alias Copi.Cornucopia.Card

    @valid_attrs %{external_id: "Rsd2", capec: [], category: "some category", description: "some description", edition: "mobileapp", language: "some language", misc: "some misc", owasp_appsensor: [], owasp_asvs: [], owasp_mastg: ["sadf"], owasp_masvs: [], owasp_scp: [], safecode: [], value: "some value", version: "some version"}
    @update_attrs %{external_id: "R2", capec: [], category: "some updated category", description: "some updated description", edition: "some updated edition", language: "some updated language", misc: "some updated misc", owasp_appsensor: [], owasp_asvs: [], owasp_mastg: [], owasp_masvs: [], owasp_scp: [], safecode: [],  value: "some updated value", version: "some updated version"}
    @invalid_attrs %{external_id: nil, capec: nil, category: nil, description: nil, edition: nil, language: nil, misc: nil, owasp_appsensor: nil, owasp_asvs: nil, owasp_mastg: nil, owasp_masvs: nil, owasp_scp: nil, safecode: nil,  value: nil, version: nil}

    def card_fixture(attrs \\ %{}) do
      {:ok, card} =
        attrs
        |> Enum.into(@valid_attrs)
        |> Cornucopia.create_card()

      card
    end

    @tag :skip
    test "list_cards/0 returns all cards" do
      card = card_fixture()
      assert Cornucopia.list_cards() == [card]
    end

    test "get_card!/1 returns the card with given id" do
      card = card_fixture()
      assert Cornucopia.get_card!(card.id) == card
    end

    test "create_card/1 with valid data creates a card" do
      assert {:ok, %Card{} = card} = Cornucopia.create_card(@valid_attrs)
      assert card.capec == []
      assert card.category == "some category"
      assert card.description == "some description"
      assert card.edition == "mobileapp"
      assert card.language == "some language"
      assert card.misc == "some misc"
      assert card.owasp_appsensor == []
      assert card.owasp_asvs == []
      assert card.owasp_scp == []
      assert card.safecode == []
      assert card.value == "some value"
      assert card.version == "some version"
    end

    test "create_card/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Cornucopia.create_card(@invalid_attrs)
    end

    test "update_card/2 with valid data updates the card" do
      card = card_fixture()
      assert {:ok, %Card{} = card} = Cornucopia.update_card(card, @update_attrs)
      assert card.capec == []
      assert card.category == "some updated category"
      assert card.description == "some updated description"
      assert card.edition == "some updated edition"
      assert card.language == "some updated language"
      assert card.misc == "some updated misc"
      assert card.owasp_appsensor == []
      assert card.owasp_asvs == []
      assert card.owasp_scp == []
      assert card.safecode == []
      assert card.value == "some updated value"
      assert card.version == "some updated version"
    end

    test "update_card/2 with invalid data returns error changeset" do
      card = card_fixture()
      assert {:error, %Ecto.Changeset{}} = Cornucopia.update_card(card, @invalid_attrs)
      assert card == Cornucopia.get_card!(card.id)
    end

    test "delete_card/1 deletes the card" do
      card = card_fixture()
      assert {:ok, %Card{}} = Cornucopia.delete_card(card)
      assert_raise Ecto.NoResultsError, fn -> Cornucopia.get_card!(card.id) end
    end

    test "change_card/1 returns a card changeset" do
      card = card_fixture()
      assert %Ecto.Changeset{} = Cornucopia.change_card(card)
    end
  end
end
