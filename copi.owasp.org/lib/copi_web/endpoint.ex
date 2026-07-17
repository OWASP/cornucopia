defmodule CopiWeb.Endpoint do
  use Phoenix.Endpoint, otp_app: :copi

  @session_max_age 7 * 24 * 60 * 60

  # The session will be stored in the cookie, encrypted, and signed.
  @session_options [
    store: CopiWeb.SessionStore,
    key: "_copi_key",
    signing_salt: "K7VwkdRe",
    encryption_salt: "vJ7hQp2L",
    http_only: true,
    secure: Mix.env() == :prod,
    same_site: "Lax",
    max_age: @session_max_age
  ]

  socket "/socket", CopiWeb.UserSocket,
    websocket: [
      timeout: 45_000,
      connect_info: [
        :peer_data,
        session: @session_options,
        x_headers: ["x-forwarded-for", "fly-client-ip"]
      ]
    ],
    longpoll: [
      connect_info: [
        :peer_data,
        session: @session_options,
        x_headers: ["x-forwarded-for", "fly-client-ip"]
      ]
    ]

  socket "/live", Phoenix.LiveView.Socket,
    websocket: [
      timeout: 45_000,
      connect_info: [
        :peer_data,
        session: @session_options,
        x_headers: ["x-forwarded-for", "fly-client-ip"]
      ]
    ],
    longpoll: [
      connect_info: [
        :peer_data,
        session: @session_options,
        x_headers: ["x-forwarded-for", "fly-client-ip"]
      ]
    ]

  # Serve at "/" the static files from "priv/static" directory.
  #
  # You should set gzip to true if you are running phx.digest
  # when deploying your static files in production.
  plug Plug.Static,
    at: "/",
    from: :copi,
    gzip: false,
    only: CopiWeb.static_paths()

  # Code reloading can be explicitly enabled under the
  # :code_reloader configuration of your endpoint.
  if code_reloading? do
    socket "/phoenix/live_reload/socket", Phoenix.LiveReloader.Socket
    plug CopiWeb.Plugs.LiveReloadSecurityHeadersPlug
    plug Phoenix.LiveReloader
    plug Phoenix.CodeReloader
    plug Phoenix.Ecto.CheckRepoStatus, otp_app: :copi
  end

  plug Phoenix.LiveDashboard.RequestLogger,
    param_key: "request_logger",
    cookie_key: "request_logger"

  plug Plug.RequestId
  plug Plug.Telemetry, event_prefix: [:phoenix, :endpoint]

  plug Plug.Parsers,
    parsers: [:urlencoded, :multipart, :json],
    pass: ["*/*"],
    json_decoder: Phoenix.json_library()

  plug Plug.MethodOverride
  plug Plug.Head
  plug Plug.Session, @session_options
  plug CopiWeb.Router
end
