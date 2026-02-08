# Generic Web Service Security

## V4.1.1

Verify that every HTTP response with a message body contains a Content-Type header field that matches the actual content of the response, including the charset parameter to specify safe character encoding (e.g., UTF-8, ISO-8859-1) according to IANA Media Types, such as "text/", "/+xml" and "/xml".

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152/index.md), [153](/taxonomy/capec-3.9/153/index.md), [160](/taxonomy/capec-3.9/160/index.md), [19](/taxonomy/capec-3.9/19/index.md), [272](/taxonomy/capec-3.9/272/index.md), [43](/taxonomy/capec-3.9/43/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## V4.1.2

Verify that only user-facing endpoints (intended for manual web-browser access) automatically redirect from HTTP to HTTPS, while other services or endpoints do not implement transparent redirects. This is to avoid a situation where a client is erroneously sending unencrypted HTTP requests, but since the requests are being automatically redirected to HTTPS, the leakage of sensitive data goes undiscovered.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [157](/taxonomy/capec-3.9/157/index.md), [39](/taxonomy/capec-3.9/39/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V4.1.3

Verify that any HTTP header field used by the application and set by an intermediary layer, such as a load balancer, a web proxy, or a backend-for-frontend service, cannot be overridden by the end-user. Example headers might include X-Real-IP, X-Forwarded-*, or X-User-ID.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [194](/taxonomy/capec-3.9/194/index.md), [22](/taxonomy/capec-3.9/22/index.md), [39](/taxonomy/capec-3.9/39/index.md), [690](/taxonomy/capec-3.9/690/index.md)

## V4.1.4

Verify that only HTTP methods that are explicitly supported by the application or its API (including OPTIONS during preflight requests) can be used and that unused methods are blocked.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [272](/taxonomy/capec-3.9/272/index.md), [28](/taxonomy/capec-3.9/28/index.md)

## V4.1.5

Verify that per-message digital signatures are used to provide additional assurance on top of transport protections for requests or transactions which are highly sensitive or which traverse a number of systems.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [145](/taxonomy/capec-3.9/145/index.md), [184](/taxonomy/capec-3.9/184/index.md), [195](/taxonomy/capec-3.9/195/index.md), [218](/taxonomy/capec-3.9/218/index.md), [39](/taxonomy/capec-3.9/39/index.md), [438](/taxonomy/capec-3.9/438/index.md), [442](/taxonomy/capec-3.9/442/index.md), [465](/taxonomy/capec-3.9/465/index.md), [475](/taxonomy/capec-3.9/475/index.md), [510](/taxonomy/capec-3.9/510/index.md), [523](/taxonomy/capec-3.9/523/index.md), [543](/taxonomy/capec-3.9/543/index.md), [594](/taxonomy/capec-3.9/594/index.md), [633](/taxonomy/capec-3.9/633/index.md), [68](/taxonomy/capec-3.9/68/index.md), [690](/taxonomy/capec-3.9/690/index.md), [75](/taxonomy/capec-3.9/75/index.md), [94](/taxonomy/capec-3.9/94/index.md), [98](/taxonomy/capec-3.9/98/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
