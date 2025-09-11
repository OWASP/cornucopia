Protect session identifiers as if they are account credentials. For HTTP cookies:

Set cookies with the HttpOnly attribute, unless you specifically require client-side scripts within your application to read or set a cookie's value.
Set the 'secure' attribute for cookies transmitted over an TLS connection.
Consider making the whole ecommerce website 'SSL-only', adding the HTTP Strict Transport Security (HSTS) header and adding the domain to web browser pre-load lists.
