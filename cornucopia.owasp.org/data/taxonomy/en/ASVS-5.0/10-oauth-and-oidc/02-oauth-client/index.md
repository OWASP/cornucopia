# OAuth Client

## V10.2.1

Verify that, if the code flow is used, the OAuth client has protection against browser-based request forgery attacks, commonly known as cross-site request forgery (CSRF), which trigger token requests, either by using proof key for code exchange (PKCE) functionality or checking the 'state' parameter that was sent in the authorization request.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115/index.md), [21](/taxonomy/capec-3.9/21/index.md), [554](/taxonomy/capec-3.9/554/index.md), [62](/taxonomy/capec-3.9/62/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.2.2

Verify that, if the OAuth client can interact with more than one authorization server, it has a defense against mix-up attacks. For example, it could require that the authorization server return the 'iss' parameter value and validate it in the authorization response and the token response.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [154](/taxonomy/capec-3.9/154/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.2.3

Verify that the OAuth client only requests the required scopes (or other authorization parameters) in requests to the authorization server.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122/index.md), [126](/taxonomy/capec-3.9/126/index.md), [143](/taxonomy/capec-3.9/143/index.md), [144](/taxonomy/capec-3.9/144/index.md), [149](/taxonomy/capec-3.9/149/index.md), [155](/taxonomy/capec-3.9/155/index.md), [203](/taxonomy/capec-3.9/203/index.md), [240](/taxonomy/capec-3.9/240/index.md), [54](/taxonomy/capec-3.9/54/index.md), [58](/taxonomy/capec-3.9/58/index.md), [633](/taxonomy/capec-3.9/633/index.md), [75](/taxonomy/capec-3.9/75/index.md), [87](/taxonomy/capec-3.9/87/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
