# OAuth Resource Server

## V10.3.1

Verify that the resource server only accepts access tokens that are intended for use with that service (audience). The audience may be included in a structured access token (such as the 'aud' claim in JWT), or it can be checked using the token introspection endpoint.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [180](/taxonomy/capec-3.9/180/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [39](/taxonomy/capec-3.9/39/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.3.2

Verify that the resource server enforces authorization decisions based on claims from the access token that define delegated authorization. If claims such as 'sub', 'scope', and 'authorization_details' are present, they must be part of the decision.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [180](/taxonomy/capec-3.9/180/index.md), [21](/taxonomy/capec-3.9/21/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.3.3

Verify that if an access control decision requires identifying a unique user from an access token (JWT or related token introspection response), the resource server identifies the user from claims that cannot be reassigned to other users. Typically, it means using a combination of 'iss' and 'sub' claims.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [180](/taxonomy/capec-3.9/180/index.md), [21](/taxonomy/capec-3.9/21/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.3.4

Verify that, if the resource server requires specific authentication strength, methods, or recentness, it verifies that the presented access token satisfies these constraints. For example, if present, using the OIDC 'acr', 'amr' and 'auth_time' claims respectively.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [180](/taxonomy/capec-3.9/180/index.md), [21](/taxonomy/capec-3.9/21/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V10.3.5

Verify that the resource server prevents the use of stolen access tokens or replay of access tokens (from unauthorized parties) by requiring sender-constrained access tokens, either Mutual TLS for OAuth 2 or OAuth 2 Demonstration of Proof of Possession (DPoP).

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [180](/taxonomy/capec-3.9/180/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [57](/taxonomy/capec-3.9/57/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
