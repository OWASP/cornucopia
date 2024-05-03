# Copi

## What is Copi?

Copi is you can play Cornucopia and Elevation of Privilege. You can play all the editions of Cornucopia  (website and mobile) as well as the Elevation of Privileges game. 


## Dev Environment Setup

If you want to contribute to Copi, follow the guide below to set up your development environment.

### Installation by Operating System
#### Mac

##### Get Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo '# Set PATH, MANPATH, etc., for Homebrew.' >> /Users/tai/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/tai/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

##### Get Elixir
```bash
brew install elixir
```

#### Linux and Windows
Follow the installation process for your [Linux distribution](https://elixir-lang.org/install.html#gnulinux) and [Windows](https://elixir-lang.org/install.html#windows). 

### Install the Elixir package manager, Hex
```bash
mix local.hex
```

#### Check you've got Elixir 1.16 and Erlang 26, or higher
```bash
elixir -v
```

### Install the web application framework, Phoenix (this line will change when 1.7 goes GA)
```bash
mix archive.install hex phx_new
```

### PostgreSQL with Docker
https://docs.docker.com/desktop/install/mac-install/

After installing docker, You can create an instance of the Postgres image:
```bash
docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=y9EAY7xeVucjM2yM -d postgres
```
Note: the password must be the same as the one in the config file of your dev environment.

You've now got Elixir, Hex, Phoenix and Postgres. You are ready to run Copi locally and contribute.

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
