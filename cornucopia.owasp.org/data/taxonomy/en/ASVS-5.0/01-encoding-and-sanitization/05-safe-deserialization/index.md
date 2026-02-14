# Safe Deserialization

## V1.5.1

Verify that the application configures XML parsers to use a restrictive configuration and that unsafe features such as resolving external entities are disabled to prevent XML eXternal Entity (XXE) attacks.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [19](/taxonomy/capec-3.9/19), [201](/taxonomy/capec-3.9/201), [23](/taxonomy/capec-3.9/23), [242](/taxonomy/capec-3.9/242), [250](/taxonomy/capec-3.9/250), [271](/taxonomy/capec-3.9/271), [66](/taxonomy/capec-3.9/66)

## V1.5.2

Verify that deserialization of untrusted data enforces safe input handling, such as using an allowlist of object types or restricting client-defined object types, to prevent deserialization attacks. Deserialization mechanisms that are explicitly defined as insecure must not be used with untrusted input.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [19](/taxonomy/capec-3.9/19), [231](/taxonomy/capec-3.9/231), [242](/taxonomy/capec-3.9/242), [250](/taxonomy/capec-3.9/250)

## V1.5.3

Verify that different parsers used in the application for the same data type (e.g., JSON parsers, XML parsers, URL parsers), perform parsing in a consistent way and use the same character encoding mechanism to avoid issues such as JSON Interoperability vulnerabilities or different URI or file parsing behavior being exploited in Remote File Inclusion (RFI) or Server-side Request Forgery (SSRF) attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [126](/taxonomy/capec-3.9/126), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [165](/taxonomy/capec-3.9/165), [175](/taxonomy/capec-3.9/175), [19](/taxonomy/capec-3.9/19), [201](/taxonomy/capec-3.9/201), [23](/taxonomy/capec-3.9/23), [242](/taxonomy/capec-3.9/242), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [272](/taxonomy/capec-3.9/272), [48](/taxonomy/capec-3.9/48), [64](/taxonomy/capec-3.9/64), [66](/taxonomy/capec-3.9/66), [664](/taxonomy/capec-3.9/664)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
