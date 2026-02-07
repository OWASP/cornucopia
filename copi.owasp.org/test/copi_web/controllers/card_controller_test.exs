defmodule CopiWeb.CardControllerTest do
  use CopiWeb.ConnCase
  alias Copi.Repo

  alias Copi.Cornucopia

  @create_attrs %{capec: [], category: "some category", description: "some description", edition: "eop", external_id: "TEST2", language: "some language", misc: "some misc", owasp_appsensor: [], owasp_asvs: [], owasp_masvs: [], biml: "", url: "", owasp_mastg: [] ,owasp_scp: [], owasp_devguide: [], safecode: [], value: "2", version: "1.0"}

  def fixture(:card) do
    Repo.delete_all(Cornucopia.Card)
    {:ok, card} = Cornucopia.create_card(@create_attrs)
    card
  end

  defp create_card(_) do
    card = fixture(:card)
    %{card: card}
  end

  describe "index" do
    setup [:create_card]
    test "lists all cards", %{conn: conn, card: card} do
      conn = get(conn, "/cards")

      response = html_response(conn, 200)
      assert response =~ card.description
    end
  end

  describe "show" do
    setup [:create_card]

    test "shows chosen card", %{conn: conn, card: card} do
      conn = get(conn, "/cards/#{card.version}/#{card.external_id}")
      response = html_response(conn, 200)
      assert response =~ card.description
    end

    test "renders 404 when card not found", %{conn: conn} do
      assert_error_sent 404, fn ->
        get(conn, "/cards/1.0/NONEXISTENT")
      end
    end
  end


end
