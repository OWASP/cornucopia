# Copi

## Dev Environment Setup (Mac)

### Get Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo '# Set PATH, MANPATH, etc., for Homebrew.' >> /Users/tai/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/tai/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Get Elixir
```bash
brew install elixir
```

### Install the Elixir package manager, Hex
```bash
mix local.hex
```

### Check you've got Elixir 1.14 and Erlang 25
```bash
elixir -v
```

### Install the web application framework, Phoenix (this line will change when 1.7 goes GA)
```bash
mix archive.install hex phx_new 1.7.0-rc.0
```

### You'll also need to get Docker for MacOS (easiest way to get a postgres instance running)
https://docs.docker.com/desktop/install/mac-install/

There's a button on the app to grab the latest stable Postgres image and run it
Click that button

You've now got Elixir, Hex, Phoenix and Postgres

Bonus: set up vscode for elixir dev https://fly.io/phoenix-files/setup-vscode-for-elixir-development/

### Clone the copi code, then
To start your Phoenix server:

  * Install dependencies with `mix deps.get`
  * Create and migrate your database with `mix ecto.setup`
  * Install Node.js dependencies with `npm install` inside the `assets` directory
  * Start Phoenix endpoint with `mix phx.server`

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](https://hexdocs.pm/phoenix/deployment.html).

## More about Phoenix

  * Official website: https://www.phoenixframework.org/
  * Guides: https://hexdocs.pm/phoenix/overview.html
  * Docs: https://hexdocs.pm/phoenix
  * Forum: https://elixirforum.com/c/phoenix-forum
  * Source: https://github.com/phoenixframework/phoenix
