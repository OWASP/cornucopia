defmodule CopiWeb.SecurityHeaders do
  def browser_headers do
    %{
      "content-security-policy" =>
        "default-src 'self'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-src 'self'; font-src 'self'; media-src 'self'; object-src 'self'; manifest-src 'self'; worker-src 'self';"
    }
  end

  def live_reload_headers do
    %{
      "content-security-policy" =>
        "default-src 'self'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-src 'self'; font-src 'self'; media-src 'self'; object-src 'self'; manifest-src 'self'; worker-src 'self';"
    }
  end
end