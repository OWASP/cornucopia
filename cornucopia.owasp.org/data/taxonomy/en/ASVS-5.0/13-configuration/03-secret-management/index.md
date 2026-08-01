# Secret Management

## V13.3.1

Verify that a secrets management solution, such as a key vault, is used to securely create, store, control access to, and destroy backend secrets. These could include passwords, key material, integrations with databases and third-party systems, keys and seeds for time-based tokens, other internal secrets, and API keys. Secrets must not be included in application source code or included in build artifacts. For an L3 application, this must involve a hardware-backed solution such as an HSM.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116), [155](/taxonomy/capec-3.9/155), [184](/taxonomy/capec-3.9/184), [188](/taxonomy/capec-3.9/188), [191](/taxonomy/capec-3.9/191), [204](/taxonomy/capec-3.9/204), [206](/taxonomy/capec-3.9/206), [207](/taxonomy/capec-3.9/207), [233](/taxonomy/capec-3.9/233), [37](/taxonomy/capec-3.9/37), [444](/taxonomy/capec-3.9/444), [445](/taxonomy/capec-3.9/445), [474](/taxonomy/capec-3.9/474), [511](/taxonomy/capec-3.9/511), [523](/taxonomy/capec-3.9/523), [548](/taxonomy/capec-3.9/548), [55](/taxonomy/capec-3.9/55), [554](/taxonomy/capec-3.9/554), [57](/taxonomy/capec-3.9/57), [639](/taxonomy/capec-3.9/639), [68](/taxonomy/capec-3.9/68)

## V13.3.2

Verify that access to secret assets adheres to the principle of least privilege.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1), [122](/taxonomy/capec-3.9/122), [155](/taxonomy/capec-3.9/155), [176](/taxonomy/capec-3.9/176), [180](/taxonomy/capec-3.9/180), [184](/taxonomy/capec-3.9/184), [204](/taxonomy/capec-3.9/204), [206](/taxonomy/capec-3.9/206), [233](/taxonomy/capec-3.9/233), [37](/taxonomy/capec-3.9/37), [444](/taxonomy/capec-3.9/444), [445](/taxonomy/capec-3.9/445), [474](/taxonomy/capec-3.9/474), [511](/taxonomy/capec-3.9/511), [523](/taxonomy/capec-3.9/523), [548](/taxonomy/capec-3.9/548), [554](/taxonomy/capec-3.9/554), [57](/taxonomy/capec-3.9/57), [58](/taxonomy/capec-3.9/58), [639](/taxonomy/capec-3.9/639), [68](/taxonomy/capec-3.9/68)

## V13.3.3

Verify that all cryptographic operations are performed using an isolated security module (such as a vault or hardware security module) to securely manage and protect key material from exposure outside of the security module.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [155](/taxonomy/capec-3.9/155), [184](/taxonomy/capec-3.9/184), [204](/taxonomy/capec-3.9/204), [206](/taxonomy/capec-3.9/206), [233](/taxonomy/capec-3.9/233), [37](/taxonomy/capec-3.9/37), [444](/taxonomy/capec-3.9/444), [445](/taxonomy/capec-3.9/445), [474](/taxonomy/capec-3.9/474), [511](/taxonomy/capec-3.9/511), [523](/taxonomy/capec-3.9/523), [548](/taxonomy/capec-3.9/548), [554](/taxonomy/capec-3.9/554), [57](/taxonomy/capec-3.9/57), [639](/taxonomy/capec-3.9/639), [68](/taxonomy/capec-3.9/68)

## V13.3.4

Verify that secrets are configured to expire and be rotated based on the application's documentation.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [180](/taxonomy/capec-3.9/180), [37](/taxonomy/capec-3.9/37), [445](/taxonomy/capec-3.9/445), [511](/taxonomy/capec-3.9/511), [554](/taxonomy/capec-3.9/554), [633](/taxonomy/capec-3.9/633)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
