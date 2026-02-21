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

[docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)

After installing docker, You can create an instance of the Postgres image:
```bash
docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=POSTGRES_LOCAL_PWD -d postgres
```
Note: the password must be the same as the one in the config file of your dev environment.

You've now got Elixir, Hex, Phoenix and Postgres. You are ready to run Copi locally and contribute.

Bonus: set up vscode for elixir dev [fly.io/phoenix-files/setup-vscode-for-elixir-development/](https://fly.io/phoenix-files/setup-vscode-for-elixir-development/)

### Clone the copi code, then

To start your Phoenix server:

  * Install dependencies with `mix deps.get`
  * Create and migrate your database with `mix ecto.setup`
  * Install Node.js dependencies with `npm install` inside the `assets` directory
  * Start Phoenix endpoint with `mix phx.server`

### Run tests

    docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=POSTGRES_LOCAL_PWD -d postgres
    export POSTGRES_TEST_PWD=POSTGRES_LOCAL_PWD
    mix test

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](https://hexdocs.pm/phoenix/deployment.html).

## More about Phoenix

  * Official website: [https://www.phoenixframework.org/](https://www.phoenixframework.org/)
  * Guides: [https://hexdocs.pm/phoenix/overview.html](https://hexdocs.pm/phoenix/overview.html)
  * Docs: [https://hexdocs.pm/phoenix](https://hexdocs.pm/phoenix)
  * Forum: [https://elixirforum.com/c/phoenix-forum](https://elixirforum.com/c/phoenix-forum)
  * Source: [https://github.com/phoenixframework/phoenix](https://github.com/phoenixframework/phoenix)

## Fly deployment

Fly.io support clustering Elixir apps which means that you can scale horizontally. [https://fly.io/docs/elixir/the-basics/clustering/](https://fly.io/docs/elixir/the-basics/clustering/)
You'll need to install elixir in order to launch the app. see: [https://github.com/OWASP/cornucopia/tree/master/copi.owasp.org#get-elixir](https://github.com/OWASP/cornucopia/tree/master/copi.owasp.org#get-elixir)
Login to fly and create a PostgreSQL cluster. See: see: [https://fly.io/dashboard/](https://fly.io/dashboard/) (Click managed postgres in the menu)
1 GB memory and 10GB storage for the db is enough.

    cd copi.owasp.org
    fly auth login
    fly launch --no-deploy

Make a note of the host and name of the app and the name of the postgresql cluster.
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
If you use get issues. See the troubleshooting section: [https://fly.io/docs/networking/custom-domain/#troubleshoot-certificate-creation](https://fly.io/docs/networking/custom-domain/#troubleshoot-certificate-creation)

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

### Heroku deploy

Set your local branch name instead of `<name>`

    git push -f heroku <name>:main
    
### Setup custom domain

    heroku domains:add copi.owaspcornucopia.org -a copiweb-stage

Then continue setting up the dns at your dns proivder: [https://devcenter.heroku.com/articles/custom-domains#configuring-dns-for-subdomains](https://devcenter.heroku.com/articles/custom-domains#configuring-dns-for-subdomains)

You'll find the dns target under

[https://dashboard.heroku.com/apps/<name>/settings](https://dashboard.heroku.com/apps/<name>/settings)

Reconfigure the apps host address

    heroku config:set PHX_HOST=copi.owaspcornucopia.org


Setup SSL on for your dns provider e.g: [https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)

    # PEM format
    heroku certs:add cloudflare.crt cloudflare.key

## Other useful things

### Statistics

Get the number of games and users per month. We do not track users. We only look at totals per month.

SELECT EXTRACT(YEAR FROM created_at) AS year, EXTRACT(MONTH FROM created_at) AS month, count(*) AS games_count FROM games WHERE created_at is not null group by year, month ORDER by year ASC, month ASC;

SELECT EXTRACT(YEAR FROM inserted_at) AS year, EXTRACT(MONTH FROM inserted_at) AS month, count(*) AS players_count FROM players WHERE inserted_at is not null group by year, month ORDER by year ASC, month ASC;

## Our Threat Model

The Copi threat model can be found at [ThreatDragonModels/copi.json](https://github.com/OWASP/cornucopia/blob/master/ThreatDragonModels/copi.json). You may review it by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard).

Here is a short summary of what you need to be aware of:

### ATJ: Mark can access resources or services because there is no authentication requirement, or it was mistakenly assumed authentication would be undertaken by some other system or performed in some previous action.

#### What can go wrong?

Be aware of data exposure risk! Copi does not support authentication.
We have not implemented Authentication when using Copi, instead we use a secure randomized string to prevent accidental data exposure. Still, an attacker may get hold of such a url by spoofing Copi or other Colleagues in your organization by leveraging various social engineering techniques like establishing a rogue location: [https://capec.mitre.org/data/definitions/616.html](https://capec.mitre.org/data/definitions/616.html).

An attacker could use various tools for capturing logs or http requests which may lead to information disclosure if your participants' network has been comporised: [https://capec.mitre.org/data/definitions/569.html](https://capec.mitre.org/data/definitions/569.html).

#### What are we going to do about it?

We are not working towards implementing authentication in Copi. Instead we are utilizing magic links. Arguable this is not authentication, but it's worth noting that your threat model is not stored on copi.owasp.org, just your game and the cards you voted on. For a threat actor to be able to piece together this information and use it against you, given that he get hold of the magic link, you would have to use your full name and, add the url to your project in the game name field when creating the game. We are working towards informing users that they should under no circumstances do this kind of thing, but even in the case that you still did. The cards themselves are two generic and doesn't contain the sensitive discussions that you had during your game.
As a security measure, you can choose to run copi on a private cluster
You should avoid using your own name or the name of a company or project when creating players and games at copi.owasp.org. And remind others not to do so as well. Instead use a pseudonyme and a fake threat model name.

### CRA: Data is not encrypted at rest by default

#### What can go wrong?

When hosting Copi yourself, be aware that the data at REST might not be encrypted. Even if you tell your threat modeling participants not to use their own name or use information about your company or project when creating the game, they may end up doing it by accident or because of a temporary lapse in memory. The data on copi.owasp.org is encrypted at rest, but if you host the game engine yourself, you need to make sure that the data is encrypted at rest as well. If you don't, an attacker that get hold of the database may be able to see the names of the players and games, which may contain sensitive information. Currently we do not use application-side encryption. Even if the data is encrypted at rest, an attacker that get hold of the database may be able to see the names of the players and games as well.

#### What are we going to do about it?

The data at REST on copi.owasp.org is encrypted by default, but we are not using client side encryption. This means that I have the possibility to access the database and see what you entered in your name fields, but I will rather quite my job then be caught snooping on your data. It would be the end of my career if I got caught doing so and the end of Copi if someone else did. When all that is said, we will implement client side encryption on Copi since I wouldn't want anyone to have the possibility to even suspect me of doing such a foolish thing (see: https://github.com/OWASP/cornucopia/issues/2232).
Ensure that your service provider ensures that the data is encrypted at REST.
OWASP host the data on Fly.io. Databases built on Fly.io uses volumes, which provide persistent storage. These drives are block-level encrypted with AES-XTS. Fly.io manages the encryption keys, ensuring they are accessible only to privileged processes running your application instances. New volumes (and thus new Postgres apps) are encrypted by default.

### CR6: Romain can read and modify unencrypted data in memory or in transit (e.g. cryptographic secrets, credentials, session identifiers, personal and commercially-sensitive data), in use or in communications within the application, or between the application and users, or between the application and external systems.

#### What can go wrong?

If deploying Copi, configure TLS between the DB and your app and between the nodes in your app cluster.
Erlang clustering does not happen over TLS by default. This may allow an attacker to launch a MTM attack and do RCE against your cluster. It may also allow an attacker to take over your database connection and both disclose sensitive information and compromise the integrity of the data sent between your database and Copi.

#### What are we going to do about it?

if you deploy Copi yourself, make sure you configure TLS appropriatly according to your needs.
OWASP host Copi on Fly.io that uses a built-in, WireGuard-encrypted 6PN (IPv6 Private Networking) mesh to automatically connect all your app instances, providing zero-config, secure, private communication with internal DNS (e.g., app-name.internal), allowing services to talk as if they're on the same network, even across regions, for simple and secure microservices communication. This mesh handles complex routing, making it easy to build distributed apps securely without manual VPN setup.

### AZ: Mike can misuse an application by using a valid feature too fast, or too frequently, or other way that is not intended, or consumes the application's resources, or causes race conditions, or over-utilizes a feature.

#### What can go wrong?

An attacker can deny access to user's by CAPEC 212, functionality misuse by continuing to create an unlimited amount of games and players until the application stops responding.

#### What are we going to do about it?

We are working on minimizing the probability of functionality misue by implementing rate limiting on the creating of games and players (see: [issues/1877](https://github.com/OWASP/cornucopia/issues/1877)). Once that is taken care of, you should be able to configure these limits to prevent DoS attacks when hosting Copi yourself. It's vital that you limit the number of sockets the application accept concurrently. On fly.io that is done in the following way: [fly.toml](https://github.com/OWASP/cornucopia/blob/fb9aae62531dde8db154729d0df4aa28a3400063/copi.owasp.org/fly.toml#L27) A 30 socket limit for Copi should allow you to handle 20.000 requests per min if you have 2 single cpu nodes.

### CK: Grant can utilize the application to deny service to some or all of its users

#### What can go wrong?

Given that  a threat actor can  execute a distributed denial of service attack against the application, he could deny access to some or all of copi.owasp.org users.

#### What are we going to do about it?

We are not working towards implementing any specific controls to prevent DoS attacks against copi.owasp.org. Most probably, it would be impossible to stop a distributed denial of service attack if executed properly. When we did load testing against copi.owasp.org, we found that the application could handle 20.000 request per min. If we went higher then that, Cloudflare, that host the DNS, would identify us as a DoS actor and return HTTP status 520. Still, conceptually, you could execute a DoS from one million machines and deny access to the application for other users. Even though this is a risk, we accept it. If you are worried about distributed DoS, please host the application on a private network or IP whitelist access to the application.
If you are hosting Copi yourself please set the rate limiting according to your needs (see: [SECURITY.md](SECURITY.md)).

### Did we do a good job?

We welcome any input or improvments you might be willing to share with us regarding our current threat model.
Arguably, we created the system before we were able to identify all these threats, and several improvements need to be made to properly balance the inherrant risks of compromise against the current security controls. For anyone choosing to host the game engine, please take this into account.
