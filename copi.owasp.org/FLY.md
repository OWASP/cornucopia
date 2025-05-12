# Fly deployment

Fly.io support clustering Elixir apps which means that you can scale horizontally. https://fly.io/docs/elixir/the-basics/clustering/

    cd copi.owasp.org
    fly auth login
    fly launch --no-deploy

Make a not of the host and name of the app.

Then deploy the app from copi.owas.org

    fly deploy --app <app name> --env PHX_HOST=<app hostname without 'https://'> --env DNS_CLUSTER_QUERY="<app name>.internal"
    fly scale count 2 --app <app name>