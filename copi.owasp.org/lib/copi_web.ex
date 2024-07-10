defmodule CopiWeb do
  @moduledoc """
  The entrypoint for defining your web interface, such
  as controllers, views, channels and so on.

  This can be used in your application as:

      use CopiWeb, :controller
      use CopiWeb, :view

  The definitions below will be executed for every view,
  controller, etc, so keep them short and clean, focused
  on imports, uses and aliases.

  Do NOT define functions inside the quoted expressions
  below. Instead, define any helper function in modules
  and import those modules here.
  """

  def controller do
    quote do
        use Phoenix.Controller,
            formats: [:html, :json],
            layouts: [html: CopiWeb.Layouts]

        import Plug.Conn
        import CopiWeb.Gettext

        unquote(verified_routes())
    end
  end

  def html do
    quote do
        use Phoenix.Component
        # Import convenience functions from controllers

        import Phoenix.Controller,
            only: [get_csrf_token: 0, view_module: 1, view_template: 1]

        # Include general helpers for rendering HTML
        unquote(html_helpers())
    end
  end

  defp html_helpers do
    quote do
        # HTML escaping functionality
        import Phoenix.HTML

        # Core UI components and translation
        import CopiWeb.CoreComponents
        import CopiWeb.GameComponents
        import CopiWeb.CoreComponents.Headers
        import CopiWeb.CoreComponents.Buttons
        import CopiWeb.CoreComponents.TableComponents
        import CopiWeb.Gettext

        # Shortcut for generating JS commands
        alias Phoenix.LiveView.JS

        # Routes generation with the ~p sigil
        unquote(verified_routes())
    end
  end

  def verified_routes do
    quote do
        use Phoenix.VerifiedRoutes,
            endpoint: CopiWeb.Endpoint,
            router: CopiWeb.Router,
            statics: CopiWeb.static_paths()
    end
  end

  def static_paths, do: ~w(assets fonts images downloads favicon.ico robots.txt)

  def live_view do
    quote do
      use Phoenix.LiveView,
        layout: {CopiWeb.Layouts, :app}

      unquote(html_helpers())
    end
  end

  def live_component do
    quote do
      use Phoenix.LiveComponent

      unquote(html_helpers())
    end
  end

  def router do
    quote do
      use Phoenix.Router

      import Plug.Conn
      import Phoenix.Controller
      import Phoenix.LiveView.Router
    end
  end

  def channel do
    quote do
      use Phoenix.Channel
      import CopiWeb.Gettext
    end
  end

  @doc """
  When used, dispatch to the appropriate controller/view/etc.
  """
  defmacro __using__(which) when is_atom(which) do
    apply(__MODULE__, which, [])
  end
end
