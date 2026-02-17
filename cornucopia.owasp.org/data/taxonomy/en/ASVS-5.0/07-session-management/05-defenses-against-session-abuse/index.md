# Defenses Against Session Abuse

## V7.5.1

Verify that the application requires full re-authentication before allowing modifications to sensitive account attributes which may affect authentication such as email address, phone number, MFA configuration, or other information used in account recovery.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114), [115](/taxonomy/capec-3.9/115), [151](/taxonomy/capec-3.9/151), [21](/taxonomy/capec-3.9/21), [50](/taxonomy/capec-3.9/50)

## V7.5.2

Verify that users are able to view and (having authenticated again with at least one factor) terminate any or all currently active sessions.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151), [195](/taxonomy/capec-3.9/195), [21](/taxonomy/capec-3.9/21), [31](/taxonomy/capec-3.9/31), [464](/taxonomy/capec-3.9/464), [465](/taxonomy/capec-3.9/465), [510](/taxonomy/capec-3.9/510), [543](/taxonomy/capec-3.9/543), [593](/taxonomy/capec-3.9/593), [98](/taxonomy/capec-3.9/98)

## V7.5.3

Verify that the application requires further authentication with at least one factor or secondary verification before performing highly sensitive transactions or operations.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114), [115](/taxonomy/capec-3.9/115), [151](/taxonomy/capec-3.9/151), [21](/taxonomy/capec-3.9/21), [49](/taxonomy/capec-3.9/49), [50](/taxonomy/capec-3.9/50)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
