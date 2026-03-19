# General Authorization Design

## V8.2.1

Verify that the application ensures that function-level access is restricted to consumers with explicit permissions.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1), [116](/taxonomy/capec-3.9/116), [122](/taxonomy/capec-3.9/122), [133](/taxonomy/capec-3.9/133), [176](/taxonomy/capec-3.9/176), [179](/taxonomy/capec-3.9/179), [180](/taxonomy/capec-3.9/180), [207](/taxonomy/capec-3.9/207), [212](/taxonomy/capec-3.9/212), [554](/taxonomy/capec-3.9/554), [58](/taxonomy/capec-3.9/58), [75](/taxonomy/capec-3.9/75)

## V8.2.2

Verify that the application ensures that data-specific access is restricted to consumers with explicit permissions to specific data items to mitigate insecure direct object reference (IDOR) and broken object level authorization (BOLA).

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122), [180](/taxonomy/capec-3.9/180), [212](/taxonomy/capec-3.9/212), [383](/taxonomy/capec-3.9/383), [58](/taxonomy/capec-3.9/58)

## V8.2.3

Verify that the application ensures that field-level access is restricted to consumers with explicit permissions to specific fields to mitigate broken object property level authorization (BOPLA).

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122), [180](/taxonomy/capec-3.9/180), [212](/taxonomy/capec-3.9/212), [383](/taxonomy/capec-3.9/383), [58](/taxonomy/capec-3.9/58)

## V8.2.4

Verify that adaptive security controls based on a consumer's environmental and contextual attributes (such as time of day, location, IP address, or device) are implemented for authentication and authorization decisions, as defined in the application's documentation. These controls must be applied when the consumer tries to start a new session and also during an existing session.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [176](/taxonomy/capec-3.9/176), [180](/taxonomy/capec-3.9/180), [195](/taxonomy/capec-3.9/195), [383](/taxonomy/capec-3.9/383), [465](/taxonomy/capec-3.9/465), [510](/taxonomy/capec-3.9/510), [543](/taxonomy/capec-3.9/543), [554](/taxonomy/capec-3.9/554), [593](/taxonomy/capec-3.9/593), [633](/taxonomy/capec-3.9/633), [98](/taxonomy/capec-3.9/98)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
