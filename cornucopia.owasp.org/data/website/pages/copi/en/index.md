# The Cornucopia Game Engine - Copi

Copi is an online place where you can play Cornucopia and Elevation of Privilege. You can play all the editions of Cornucopia (website and mobile) as well as the Elevation of Privileges game. To just play, visit: https://copi.owasp.org

![The Cornucopia Game Engine - Copi](copi.png)

## Dev Environment Setup

If you want to contribute to Copi, follow the guide below to set up your development environment.

But first...

```bash
git clone https://github.com/owasp/cornucopia
cd cornucopia/copi.owasp.org
```

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

[docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)

After installing docker, You can create an instance of the Postgres image:

```bash
openssl rand -base64 32 # please note the output. E.g: 5xpdhzomIy4Di+UFw/r7SJSb7pvQhPitXGoet7fbMCY=
# Linux
export COPI_ENCRYPTION_KEY="5xpdhzomIy4Di+UFw/r7SJSb7pvQhPitXGoet7fbMCY="
export POSTGRES_PASSWORD=POSTGRES_LOCAL_PWD
# Windows
# $env:COPI_ENCRYPTION_KEY="5xpdhzomIy4Di+UFw/r7SJSb7pvQhPitXGoet7fbMCY="
# $env:POSTGRES_PASSWORD="POSTGRES_LOCAL_PWD"
# $env:POSTGRES_PASSWORD="POSTGRES_LOCAL_PWD"

docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=POSTGRES_LOCAL_PWD -d postgres
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

```bash
docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=POSTGRES_LOCAL_PWD -d postgres
# Linux
export POSTGRES_TEST_PWD=POSTGRES_LOCAL_PWD
# Windows
# $env:POSTGRES_TEST_PWD="POSTGRES_LOCAL_PWD"
mix test
mix assets.coverage
```

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](https://hexdocs.pm/phoenix/deployment.html).

## Player session and replay storage

Copi uses encrypted cookie sessions and single-node, in-memory capability replay protection by default. This mode does not store player sessions or capability digests in PostgreSQL.

When `DNS_CLUSTER_QUERY` is set, replay registries coordinate through a globally registered Erlang process. A node falls back to its local registry if the global process cannot be reached and synchronizes its active digests when the connection returns. A capability can still be accepted on both sides of a network partition before that synchronization happens.

PostgreSQL-backed player sessions and replay protection are optional:

```bash
POSTGRES_SESSION_STORE_ENABLED=true
```

When enabled, the browser cookie contains an opaque session ID protected by the normal Phoenix cookie encryption. The player session written to the `copi_sessions` table is separately encrypted with `COPI_ENCRYPTION_KEY`. Consumed capability digests are inserted atomically into `player_capability_consumptions`, so nodes using the same database share replay protection. PostgreSQL mode takes precedence over the in-memory and clustered replay registries.

Run the database migrations before enabling this option. Configure every application node with the same setting, `SECRET_KEY_BASE`, and `COPI_ENCRYPTION_KEY`. `COPI_ENCRYPTION_KEY` is used for session encryption only when state is written to or read from PostgreSQL; browser cookies continue to use Phoenix's `SECRET_KEY_BASE`. Protect database connections with verified TLS when the database is not on a trusted local network. If PostgreSQL is unavailable, session loading and capability exchange fail rather than falling back to a weaker store.

Changing the storage mode invalidates existing browser sessions. Capability exchange tokens remain valid for 5 minutes and player sessions remain valid for up to 7 days in every mode.

## More about Phoenix

  * Official website: https://www.phoenixframework.org/
  * Guides: https://hexdocs.pm/phoenix/overview.html
  * Docs: https://hexdocs.pm/phoenix
  * Forum: https://elixirforum.com/c/phoenix-forum
  * Source: https://github.com/phoenixframework/phoenix

## Fly deployment

Fly.io support clustering Elixir apps which means that you can scale horizontally. https://fly.io/docs/elixir/the-basics/clustering/
You'll need to install elixir in order to launch the app. see: https://github.com/OWASP/cornucopia/tree/master/copi.owasp.org#get-elixir
Login to fly and create a PostgreSQL cluster. see: https://fly.io/dashboard/ (Click managed postgres in the menu)
1 GB memory and 10GB storage for the db is enough.

    cd copi.owasp.org
    fly auth login
    fly launch --no-deploy

Make a note of the host and name of the app and the name of the postgresql cluster.
Then deploy the app from `./copi.owasp.org`

```bash
    fly mpg attach <cluster name> --app <app name>
    fly deploy --app <app name> --env PHX_HOST=<app hostname without 'https://'>
    fly scale count 2 --app <app name>
```

### Setting up the encryption key on Fly.io

Generate a secure encryption key:

    openssl rand -base64 32

Set it as a secret environment variable on Fly.io:

    fly secrets set COPI_ENCRYPTION_KEY=<your-generated-key> --app <app name>

### Fly setup custom domain name

```bash
    fly certs add copi.owasp.org
```

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

```bash
heroku login
heroku apps:create --addons heroku-postgresql:essential-0 --region eu -b https://github.com/negativetwelve/heroku-buildpack-subdir -s heroku-22
heroku apps:rename <name> --app <old name>
git remote set-url heroku https://git.heroku.com/<name>.git
heroku config:set PHX_HOST=<name>-*.herokuapp.com
```

### Heroku App Setup

```bash
heroku config:set ECTO_SSL_VERIFY=false
heroku config:set SECRET_KEY_BASE=$(mix phx.gen.secret)
heroku config:set POOL_SIZE=18
heroku config:set PROJECT_PATH=copi.owasp.org # points to the subdirectory in
```

### Setting up the encryption key on Heroku

Generate a secure encryption key:

    openssl rand -base64 32

Set it as an environment variable on Heroku:

    heroku config:set COPI_ENCRYPTION_KEY=<your-generated-key>

### Heroku deploy

Set your local branch name instead of `<name>`

```bash
git push -f heroku <name>:main
```
    
### Setup custom domain

```bash
heroku domains:add copi.owaspcornucopia.org -a copiweb-stage
```

Then continue setting up the dns at your dns proivder: https://devcenter.heroku.com/articles/custom-domains#configuring-dns-for-subdomains

You'll find the dns target under

https://dashboard.heroku.com/apps/<name>/settings

Reconfigure the apps host address

```bash
heroku config:set PHX_HOST=copi.owaspcornucopia.org
```

Setup SSL on for your dns provider e.g: https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/

```bash
# PEM format
heroku certs:add cloudflare.crt cloudflare.key
```

## Our Threat Model

The Copi threat model can be found at [ThreatDragonModels/copi.json](https://github.com/OWASP/cornucopia/blob/master/ThreatDragonModels/copi.json). You may review it by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard).

Please also read [SECURITY.md](https://github.com/OWASP/cornucopia/blob/master/copi.owasp.org/SECURITY.md) to ensure you have taken the appropriate measures to secure Copi if you are running the service yourself.

Here is a short summary of what you need to be aware of:

### ATJ: Anyone with a game link can watch the game

#### What can go wrong?

Copi does not use user accounts. Anyone with a game link can watch that game. This is intended.

Someone may obtain a game link, a short-lived player capability, or a player session cookie through social engineering, logs, a compromised browser, or a compromised network. See [CAPEC-616](https://capec.mitre.org/data/definitions/616.html) and [CAPEC-569](https://capec.mitre.org/data/definitions/569.html).

Watching a game does not grant player access. Player access requires a signed capability that expires after 5 minutes. If someone steals that capability before it is used, they may exchange it and become that player. The capability is sent in a POST body, so a proxy or monitoring service that records request bodies may capture it.

By default, Copi remembers used capabilities in the memory of one application node. That record is lost when the node restarts. In a cluster, nodes normally share this check through one global registry. If the nodes lose contact, each node uses its own local record. The same capability may then be accepted by more than one node. Synchronizing the records later cannot undo an exchange that has already succeeded.

An optional PostgreSQL mode avoids these replay gaps by keeping the session and replay records in one database. This makes player sessions depend on the database being available. The session records are encrypted, but anyone who obtains both the database contents and `COPI_ENCRYPTION_KEY` can read them.

The player session cookie is a bearer credential. Anyone who steals a valid copy can act as every player stored in that session until it expires. In the default cookie mode, an individual stolen session cannot be revoked. In PostgreSQL mode, deleting the server-side session record revokes it.

Voting and card play still have race conditions. The votes table has no uniqueness constraint, so two requests made at nearly the same time may create duplicate votes. The database also has no rule that limits a player to one played card per round, so concurrent requests may play more than one card.

#### What are we going to do about it?

Use HTTPS. Do not record capability exchange request bodies in proxies, application monitoring, or access logs. Protect `SECRET_KEY_BASE` and `COPI_ENCRYPTION_KEY`, and rotate the affected key if it is exposed.

Use PostgreSQL session storage when a capability must be accepted only once across several application nodes. Restrict access to the session tables and use verified TLS for the database connection. Without PostgreSQL mode, accept that a restart or cluster partition can allow a capability to be reused during its 5-minute lifetime.

Copi stores game and card choices, but not the discussion held by the players. Do not use a real person, company, or project name for a game or player. Use a pseudonym and a made-up threat model name.

Run Copi on a private network if viewing by game link is not suitable for your use case.

Voting integrity is tracked in [issue 2568](https://github.com/OWASP/cornucopia/issues/2568).

## CR6: Romain can read and modify unencrypted data in memory or in transit (e.g., cryptographic secrets, credentials, session identifiers, personal and commercially-sensitive data), in use or in communications within the application, or between the application and users, or between the application and external systems.

#### What can go wrong?

Production database transport security is not safely configured by default. The DB SSL option is set at startup to either false or verify_none, and the app applies that value directly to the Repo. In other words, the current code path never enables verified TLS to Postgres by default. If the database is not strictly local/private, credentials and application data can be exposed or modified in transit.
If deploying Copi, configure TLS between the DB and your app and between the nodes in your app cluster.
Erlang clustering does not happen over TLS by default. This may allow an attacker to launch a MTM attack and do RCE against your cluster. It may also allow an attacker to take over your database connection and both disclose sensitive information and compromise the integrity of the data sent between your database and Copi.

Cookie and TLS hardening still depend on deployment discipline rather than being enforced by the app. The repo ships a fixed secret_key_base in config.exs, the session cookie is only marked secure during app start-up, and HTTPS enforcement is only documented, not enabled by default. If a staging or self-hosted deployment ever runs outside strict prod/TLS settings, session confidentiality and integrity may degrade quickly.

#### What are we going to do about it?

If you deploy Copi yourself, make sure you configure TLS appropriately according to your needs.
OWASP host Copi on Fly.io that uses a built-in, WireGuard-encrypted 6PN (IPv6 Private Networking) mesh to automatically connect all your app instances, providing zero-config, secure, private communication with internal DNS (e.g., app-name.internal), allowing services to talk as if they're on the same network, even across regions, for simple and secure microservices communication. This mesh handles complex routing, making it easy to build distributed apps securely without manual VPN setup.

### AZ: Mike can misuse an application by using a valid feature too fast, or too frequently, or in any other way that is not intended, or consumes the application's resources, or causes race conditions, or over-utilizes a feature.

#### What can go wrong?

An attacker can deny access to user's by CAPEC 212, functionality misuse by continuing to create an unlimited amount of games and players until the application stops responding.

The current rate-limiting design is easy to evade in common proxy or multi-instance deployments. The rate limiting trusts the left-most X-Forwarded-For value and explicitly skips connection limiting when only remote_ip is available. The counters are kept in the in-memory GenServer. That means spoofed forwarded headers, multiple app nodes, or proxy/header misconfiguration can let an attacker bypass the main abuse-control mechanism. We are more than happy to get suggestions for how to improve the rate-limiting. Currently we are not seeing a lot of issues concerning the misuse of our services in production.

The Fly.io reverse proxy does not strip or rewrite untrusted X-Forwarded-For headers before traffic reaches Phoenix. It is therefore still possible to circumvent the rate-limiter.

#### What are we going to do about it?

We are working on minimizing the probability of functionality misuse by implementing rate limiting on the creation of games and players (see: [issues/1877](https://github.com/OWASP/cornucopia/issues/1877)). Once that is taken care of, you should be able to configure these limits to prevent DoS attacks when hosting Copi yourself. It's vital that you limit the number of sockets the application accepts concurrently. On fly.io that is done in the following way: [fly.toml](https://github.com/OWASP/cornucopia/blob/fb9aae62531dde8db154729d0df4aa28a3400063/copi.owasp.org/fly.toml#L27) A 30 socket limit for Copi should allow you to handle 20.000 requests per min if you have 2 single cpu nodes Which we have tested against that setup.

When Copi receives traffic directly from Fly Proxy, set `USE_FLY_CLIENT_IP=true`. [Fly.io documents `Fly-Client-IP`](https://fly.io/docs/networking/request-headers/#fly-client-ip) as the client IP address from Fly Proxy's perspective and says it may be a better choice than `X-Forwarded-For`, which must be treated with caution to avoid spoofing. Using it prevents Copi's rate limiter from trusting a client-controlled, left-most `X-Forwarded-For` value. If another reverse proxy is in front of Fly.io, `Fly-Client-IP` contains that proxy's address instead of the original client's address; in that deployment, parse `X-Forwarded-For` using an explicit trusted-proxy configuration.

### CK: Grant can utilize the application to deny service to some or all of its users

#### What can go wrong?

Given that  a threat actor can  execute a distributed denial of service attack against the application, he could deny access to some or all of copi.owasp.org users.

#### What are we going to do about it?

We are not working towards implementing any specific controls to prevent DoS attacks against copi.owasp.org. Most probably, it would be impossible to stop a distributed denial of service attack if executed properly. When we did load testing against copi.owasp.org, we found that the application could handle 20.000 request per min. If we went higher than that, Cloudflare, which hosts the DNS, would identify us as a DoS actor and return HTTP status 520. Still, conceptually, you could execute a DoS from one million machines and deny access to the application for other users. Even though this is a risk, we accept it. If you are worried about distributed DoS, please host the application on a private network or whitelist IP access to the application.
If you are hosting Copi yourself, please set the rate limiting according to your needs (see: [Configuration](https://github.com/OWASP/cornucopia/blob/master/copi.owasp.org/SECURITY.md#configuration)).

### Did we do a good job?

We welcome any input or improvements you might be willing to share with us regarding our current threat model.
Arguably, we created the system before we were able to identify all these threats, and several improvements need to be made to properly balance the inherent risks of compromise against the current security controls. For anyone choosing to host the game engine, please take this into account.
