defmodule CopiWeb.CardView do
  use CopiWeb, :view

  def format_capec(refs) do
    refs
    |> Enum.map(fn ref ->
      link(ref, to: "https://capec.mitre.org/data/definitions/#{ref}.html")
    end)
    |> Enum.intersperse(", ")
  end
end
