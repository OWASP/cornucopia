defmodule CopiWeb.CardController do
  use CopiWeb, :controller

  alias Copi.Cornucopia

  def index(conn, _params) do
    cards = Cornucopia.list_cards()
    render(conn, "index.html", cards: cards)
  end

  def show(conn, %{"version" => version, "id" => id}) do
    card = Cornucopia.get_card_by_external_id!(version, id)
    render(conn, "show.html", card: card)
  end

  @spec format_capec(any()) :: any()
  def format_capec(refs) do
    refs
    #|> Enum.map(fn ref -> link(ref, to: "https://capec.mitre.org/data/definitions/#{ref}.html") end)
    #|> Enum.intersperse(", ")
  end
end
