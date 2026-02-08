# Authentication with an Identity Provider

## V6.8.1

Verify that, if the application supports multiple identity providers (IdPs), the user's identity cannot be spoofed via another supported identity provider (eg. by using the same user identifier). The standard mitigation would be for the application to register and identify the user using a combination of the IdP ID (serving as a namespace) and the user's ID in the IdP.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md)

## V6.8.2

Verify that the presence and integrity of digital signatures on authentication assertions (for example on JWTs or SAML assertions) are always validated, rejecting any assertions that are unsigned or have invalid signatures.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md), [268](/taxonomy/capec-3.9/268/index.md), [473](/taxonomy/capec-3.9/473/index.md), [475](/taxonomy/capec-3.9/475/index.md)

## V6.8.3

Verify that SAML assertions are uniquely processed and used only once within the validity period to prevent replay attacks.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md), [151](/taxonomy/capec-3.9/151/index.md), [50](/taxonomy/capec-3.9/50/index.md), [633](/taxonomy/capec-3.9/633/index.md)

## V6.8.4

Verify that, if an application uses a separate Identity Provider (IdP) and expects specific authentication strength, methods, or recentness for specific functions, the application verifies this using the information returned by the IdP. For example, if OIDC is used, this might be achieved by validating ID Token claims such as 'acr', 'amr', and 'auth_time' (if present). If the IdP does not provide this information, the application must have a documented fallback approach that assumes that the minimum strength authentication mechanism was used (for example, single-factor authentication using username and password).

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114/index.md), [115](/taxonomy/capec-3.9/115/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
