defmodule CopiWeb.CardController do
  use CopiWeb, :controller

  alias Copi.Cornucopia

  def index(conn, _params) do
    cards = Cornucopia.list_cards()
    render(conn, "index.html", cards: cards)
  end

  def show(conn, %{"id" => id}) do
    card = Cornucopia.get_card!(id)
    render(conn, "show.html", card: card)
  end
end
