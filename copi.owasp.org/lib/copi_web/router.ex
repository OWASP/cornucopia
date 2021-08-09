defmodule CopiWeb.Router do
  use CopiWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, {CopiWeb.LayoutView, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CopiWeb do
    pipe_through :browser

    live "/", PageLive, :index

    live "/games", GameLive.Index, :index
    live "/games/new", GameLive.Index, :new
    live "/games/:game_id", GameLive.Show, :show

    live "/games/:game_id/players", PlayerLive.Index, :index
    live "/games/:game_id/players/new", PlayerLive.Index, :new

    live "/games/:game_id/players/:id", PlayerLive.Show, :show

    resources "/cards", CardController
  end

  scope "/api", CopiWeb do
    pipe_through :api

    put "/games/:game_id/players/:player_id/card", ApiController, :play_card
  end

  # Other scopes may use custom stacks.
  # scope "/api", CopiWeb do
  #   pipe_through :api
  # end

  # Enables LiveDashboard only for development
  #
  # If you want to use the LiveDashboard in production, you should put
  # it behind authentication and allow only admins to access it.
  # If your application does not have an admins-only section yet,
  # you can use Plug.BasicAuth to set up some basic authentication
  # as long as you are also using SSL (which you should anyway).
  if Mix.env() in [:dev, :test] do
    import Phoenix.LiveDashboard.Router

    scope "/" do
      pipe_through :browser
      live_dashboard "/dashboard", metrics: CopiWeb.Telemetry
    end
  end
end
