# Heroku Infra setup

No support for clustering. The app won't work properly if you configure more then one dyno.

    heroku login
    heroku apps:create --addons heroku-postgresql:essential-0 --region eu -b https://github.com/negativetwelve/heroku-buildpack-subdir -s heroku-22
    heroku apps:rename copiweb --app <old name>
    git remote set-url heroku https://git.heroku.com/copiweb.git
    heroku config:set PHX_HOST=<rest of host name>-*.herokuapp.com

Then setup access to the api key  by creating an org secret in github with the following name:

    OWASP_HEROKU_API_KEY

Deploy the code, the. afterwards, the domain needs to be setup like this:

    heroku domains:add copi.owasp.org -a copiweb

Then continue setting up the dns at cloudflare: https://devcenter.heroku.com/articles/custom-domains#configuring-dns-for-subdomains

https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-subdomain/

You'll find the dns target under

https://dashboard.heroku.com/apps/copiweb/settings

Reconfigure the apps host address

heroku config:set PHX_HOST=copi.owasp.org

Setup SSL between heorku and cloudflare e.g: https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/

    # PEM format
    heroku certs:add cloudflare.crt cloudflare.key
