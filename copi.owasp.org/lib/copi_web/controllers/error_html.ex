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
    status = assigns[:status] || 500
    status_template = if function_exported?(__MODULE__, String.to_atom(to_string(status)), 1) do
      String.to_atom(to_string(status))
    else
      :"500"
    end

    #Phoenix.Controller.status_message_from_template(template)
    apply(__MODULE__, status_template, [assigns])
  end

end
