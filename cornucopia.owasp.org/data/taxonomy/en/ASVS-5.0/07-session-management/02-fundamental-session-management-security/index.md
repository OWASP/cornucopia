# Fundamental Session Management Security

## V7.2.1

Verify that the application performs all session token verification using a trusted, backend service.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [115](/taxonomy/capec-3.9/115), [196](/taxonomy/capec-3.9/196), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [31](/taxonomy/capec-3.9/31), [554](/taxonomy/capec-3.9/554), [59](/taxonomy/capec-3.9/59), [61](/taxonomy/capec-3.9/61)

## V7.2.2

Verify that the application uses either self-contained or reference tokens that are dynamically generated for session management, i.e. not using static API secrets and keys.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [21](/taxonomy/capec-3.9/21), [31](/taxonomy/capec-3.9/31), [59](/taxonomy/capec-3.9/59), [61](/taxonomy/capec-3.9/61)

## V7.2.3

Verify that if reference tokens are used to represent user sessions, they are unique and generated using a cryptographically secure pseudo-random number generator (CSPRNG) and possess at least 128 bits of entropy.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [196](/taxonomy/capec-3.9/196), [21](/taxonomy/capec-3.9/21), [31](/taxonomy/capec-3.9/31), [59](/taxonomy/capec-3.9/59)

## V7.2.4

Verify that the application generates a new session token on user authentication, including re-authentication, and terminates the current session token.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [21](/taxonomy/capec-3.9/21), [31](/taxonomy/capec-3.9/31), [59](/taxonomy/capec-3.9/59), [593](/taxonomy/capec-3.9/593)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
