# Fly deployment

Fly.io support clustering Elixir apps which means that you can scale horizontally. https://fly.io/docs/elixir/the-basics/clustering/

    cd copi.owasp.org
    fly launch --no-deploy

Login and go to your new app
Change the following environment variables under  `[env]` in [fly.toml](fly.toml) 

    PHX_HOST = <hostname for the app without 'https://'>
    DNS_CLUSTER_QUERY = "<name of the app>.internal"

Then deploy the app from copi.owas.org

    fly deploy
    fly scale count 2