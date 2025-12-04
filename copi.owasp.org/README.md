# Copi

## What is Copi?

Copi is an online place where you can play Cornucopia and Elevation of Privilege. You can play all the editions of Cornucopia  (website and mobile) as well as the Elevation of Privileges game.


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

#### Check you've got Elixir 1.18 and Erlang 27, or higher
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

### Run tests

    docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=y9EAY7xeVucjM2yM -d postgres
    export POSTGRES_TEST_PWD=y9EAY7xeVucjM2yM
    mix test
  *

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

## Security Features

### Rate Limiting

Copi implements IP-based rate limiting to protect against abuse and ensure availability for all users. This addresses CAPEC 212 (Functionality Misuse) attacks.

**Features:**
- **Game Creation Limiting**: Limits the number of games that can be created from a single IP address
- **Connection Limiting**: Limits the number of WebSocket connections from a single IP address
- **Configurable Limits**: All limits and time windows are configurable via environment variables

**Configuration:**

Set the following environment variables to customize rate limits:

```bash
# Maximum games per IP (default: 10)
export MAX_GAMES_PER_IP=10

# Time window for game creation in seconds (default: 3600 = 1 hour)
export GAME_CREATION_WINDOW_SECONDS=3600

# Maximum connections per IP (default: 50)
export MAX_CONNECTIONS_PER_IP=50

# Time window for connections in seconds (default: 300 = 5 minutes)
export CONNECTION_WINDOW_SECONDS=300
```

**How it works:**
- The rate limiter tracks requests by IP address
- When a limit is exceeded, users receive a clear error message with a retry time
- Expired entries are automatically cleaned up every 5 minutes
- Rate limits are independent for game creation vs. connections
- The system handles both IPv4 and IPv6 addresses
- X-Forwarded-For headers are respected for reverse proxy deployments

**For Reverse Proxy Deployments:**

If deploying behind a reverse proxy (nginx, Apache, Cloudflare, etc.), ensure the proxy passes the real client IP:

```nginx
# Nginx example
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

Ready to run in production? Please [check our deployment guides](https://hexdocs.pm/phoenix/deployment.html).

## More about Phoenix

  * Official website: https://www.phoenixframework.org/
  * Guides: https://hexdocs.pm/phoenix/overview.html
  * Docs: https://hexdocs.pm/phoenix
  * Forum: https://elixirforum.com/c/phoenix-forum
  * Source: https://github.com/phoenixframework/phoenix

## Fly deployment

Fly.io support clustering Elixir apps which means that you can scale horizontally. https://fly.io/docs/elixir/the-basics/clustering/
You'll need to install elixir in order to launch the app. see: https://github.com/OWASP/cornucopia/tree/master/copi.owasp.org#get-elixir
Login to fly and create a PostgreSQL cluster. See: see: https://fly.io/dashboard/ (Click managed postgres in the menu)
1 GB memory and 10GB storage for the db is enough.

    cd copi.owasp.org
    fly auth login
    fly launch --no-deploy

Make a note of the host and name of the app and the name of the postgresql cluster.

Configure rate limiting (optional, uses defaults if not set):

    fly secrets set MAX_GAMES_PER_IP=10 --app <app name>
    fly secrets set GAME_CREATION_WINDOW_SECONDS=3600 --app <app name>
    fly secrets set MAX_CONNECTIONS_PER_IP=50 --app <app name>
    fly secrets set CONNECTION_WINDOW_SECONDS=300 --app <app name>

Then deploy the app from `./copi.owasp.org`

    fly mpg attach <cluster name> --app <app name>
    fly deploy --app <app name> --env PHX_HOST=<app hostname without 'https://'>
    fly scale count 2 --app <app name>

### Fly setup custom domain name

    fly certs add copi.owasp.org

Setup A and AAAA record in Cloudflare

Go to https://fly.io/apps/<app name>/certificates/copi.owasp.org

You'll need to add both the A and AAAA records together with the CNAME challenge to cloudflare.
NB: The challenge should not be proxied through cloudflare!
Please allow for 30 min for the change to take effect, but check that the "Domain ownership verification" went ok. 

Follow the instructions given.
If you use get issues. See the troubleshooting section: https://fly.io/docs/networking/custom-domain/#troubleshoot-certificate-creation

## Heroku deployment

No support for clustering. The app won't work properly if you configure more then one dyno.

### Heroku Infra Setup

Set your prefered app name instead of `<name>`

    heroku login
    heroku apps:create --addons heroku-postgresql:essential-0 --region eu -b https://github.com/negativetwelve/heroku-buildpack-subdir -s heroku-22
    heroku apps:rename <name> --app <old name>
    git remote set-url heroku https://git.heroku.com/<name>.git
    heroku config:set PHX_HOST=<name>-*.herokuapp.com


### Heroku App Setup

    heroku config:set ECTO_SSL_VERIFY=false
    heroku config:set SECRET_KEY_BASE=$(mix phx.gen.secret)
    heroku config:set POOL_SIZE=18
    heroku config:set PROJECT_PATH=copi.owasp.org # points to the subdirectory
    
    # Optional: Configure rate limiting (uses defaults if not set)
    heroku config:set MAX_GAMES_PER_IP=10
    heroku config:set GAME_CREATION_WINDOW_SECONDS=3600
    heroku config:set MAX_CONNECTIONS_PER_IP=50
    heroku config:set CONNECTION_WINDOW_SECONDS=300

### Heroku deploy

Set your local branch name instead of `<name>`

    git push -f heroku <name>:main
    
### Setup custom domain

    heroku domains:add copi.owaspcornucopia.org -a copiweb-stage

Then continue setting up the dns at your dns proivder: https://devcenter.heroku.com/articles/custom-domains#configuring-dns-for-subdomains

You'll find the dns target under

https://dashboard.heroku.com/apps/<name>/settings

Reconfigure the apps host address

    heroku config:set PHX_HOST=copi.owaspcornucopia.org


Setup SSL on for your dns provider e.g: https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/

    # PEM format
    heroku certs:add cloudflare.crt cloudflare.key