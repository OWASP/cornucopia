# Generic OAuth and OIDC Security

## V10.1.1

Verify that tokens are only sent to components that strictly need them. For example, when using a backend-for-frontend pattern for browser-based JavaScript applications, access and refresh tokens shall only be accessible for the backend.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115/index.md), [180](/taxonomy/capec-3.9/180/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [554](/taxonomy/capec-3.9/554/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.1.2

Verify that the client only accepts values from the authorization server (such as the authorization code or ID Token) if these values result from an authorization flow that was initiated by the same user agent session and transaction. This requires that client-generated secrets, such as the proof key for code exchange (PKCE) 'code_verifier', 'state' or OIDC 'nonce', are not guessable, are specific to the transaction, and are securely bound to both the client and the user agent session in which the transaction was started.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115/index.md), [180](/taxonomy/capec-3.9/180/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [554](/taxonomy/capec-3.9/554/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
