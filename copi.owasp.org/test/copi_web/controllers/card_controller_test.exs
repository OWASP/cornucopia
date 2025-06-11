defmodule CopiWeb.CardControllerTest do
  use CopiWeb.ConnCase
  alias Copi.Repo

  alias Copi.Cornucopia

  @create_attrs %{capec: [], category: "some category", description: "some description", edition: "eop", external_id: "TEST2", language: "some language", misc: "some misc", owasp_appsensor: [], owasp_asvs: [], owasp_masvs: [], biml: "", owasp_mastg: [] ,owasp_scp: [], safecode: [], value: "2", version: "1.0"}

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
      IO.inspect(response, limit: :infinity)
      assert response =~ card.description
    end
  end


end
