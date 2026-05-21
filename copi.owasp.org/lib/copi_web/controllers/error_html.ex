defmodule CopiWeb.ErrorHTML do
  use CopiWeb, :html

  # If you want to customize your error pages,
  # uncomment the embed_templates/1 call below
  # and add pages to the error directory:
  #
  #   * lib/hello_web/controllers/error/404.html.heex
  #   * lib/hello_web/controllers/error/500.html.heex
  #
  embed_templates "error_html/*"

  # The default is to render a plain text page based on
  # the template name. For example, "404.html" becomes
  # "Not Found".
  def render(template, assigns) do
    # Derive the status code from the template name (e.g. "400.html" -> :"400")
    status_template =
      case String.split(template, ".") do
        [status | _] ->
          atom = String.to_atom(status)
          if function_exported?(__MODULE__, atom, 1), do: atom, else: :"500"
        _ ->
          :"500"
      end

    apply(__MODULE__, status_template, [assigns])
  end

end
