# General TLS Security Guidance

## V12.1.1

Verify that only the latest recommended versions of the TLS protocol are enabled, such as TLS 1.2 and TLS 1.3. The latest version of the TLS protocol must be the preferred option.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [31](/taxonomy/capec-3.9/31), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [593](/taxonomy/capec-3.9/593), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## V12.1.2

Verify that only recommended cipher suites are enabled, with the strongest cipher suites set as preferred. L3 applications must only support cipher suites which provide forward secrecy.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## V12.1.3

Verify that the application validates that mTLS client certificates are trusted before using the certificate identity for authentication or authorization.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [633](/taxonomy/capec-3.9/633), [65](/taxonomy/capec-3.9/65), [94](/taxonomy/capec-3.9/94)

## V12.1.4

Verify that proper certification revocation, such as Online Certificate Status Protocol (OCSP) Stapling, is enabled and configured.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [65](/taxonomy/capec-3.9/65), [89](/taxonomy/capec-3.9/89), [94](/taxonomy/capec-3.9/94)

## V12.1.5

Verify that Encrypted Client Hello (ECH) is enabled in the application's TLS settings to prevent exposure of sensitive metadata, such as the Server Name Indication (SNI), during TLS handshake processes.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [102](/taxonomy/capec-3.9/102), [117](/taxonomy/capec-3.9/117), [217](/taxonomy/capec-3.9/217), [220](/taxonomy/capec-3.9/220), [65](/taxonomy/capec-3.9/65), [89](/taxonomy/capec-3.9/89), [94](/taxonomy/capec-3.9/94)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
