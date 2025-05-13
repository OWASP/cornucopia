# Fly deployment

Fly.io support clustering Elixir apps which means that you can scale horizontally. https://fly.io/docs/elixir/the-basics/clustering/

    cd copi.owasp.org
    fly auth login
    fly launch --no-deploy

Make a note of the host and name of the app.

Then deploy the app from copi.owas.org

    fly deploy --app <app name> --env PHX_HOST=<app hostname without 'https://'> --env DNS_CLUSTER_QUERY="<app name>.internal"
    fly scale count 2 --app <app name>

## Fly setup custom domain name

    fly certs add copi.owasp.org

Setup A and AAAA record in Cloudflare

Go to https://fly.io/apps/<app name>/certificates/copi.owasp.org

You'll need to add both the A and AAAA records together with the CNAME challenge to cloudflare.
NB: The challenge should not be proxied through cloudflare!
Please allow for 30 min for the change to take effect, but check that the "Domain ownership verification" went ok. 

Follow the instructions given.
If you use get issues. See the troubleshooting section: https://fly.io/docs/networking/custom-domain/#troubleshoot-certificate-creation