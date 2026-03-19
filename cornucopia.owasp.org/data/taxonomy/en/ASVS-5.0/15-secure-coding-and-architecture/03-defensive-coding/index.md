# Defensive Coding

## V15.3.1

Verify that the application only returns the required subset of fields from a data object. For example, it should not return an entire data object, as some individual fields should not be accessible to users.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [122](/taxonomy/capec-3.9/122), [137](/taxonomy/capec-3.9/137), [212](/taxonomy/capec-3.9/212), [261](/taxonomy/capec-3.9/261), [28](/taxonomy/capec-3.9/28), [58](/taxonomy/capec-3.9/58)

## V15.3.2

Verify that where the application backend makes calls to external URLs, it is configured to not follow redirects unless it is intended functionality.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [137](/taxonomy/capec-3.9/137), [154](/taxonomy/capec-3.9/154), [19](/taxonomy/capec-3.9/19), [240](/taxonomy/capec-3.9/240), [261](/taxonomy/capec-3.9/261), [28](/taxonomy/capec-3.9/28), [481](/taxonomy/capec-3.9/481)

## V15.3.3

Verify that the application has countermeasures to protect against mass assignment attacks by limiting allowed fields per controller and action, e.g., it is not possible to insert or update a field value when it was not intended to be part of that action.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [130](/taxonomy/capec-3.9/130), [137](/taxonomy/capec-3.9/137), [162](/taxonomy/capec-3.9/162), [19](/taxonomy/capec-3.9/19), [212](/taxonomy/capec-3.9/212), [261](/taxonomy/capec-3.9/261), [28](/taxonomy/capec-3.9/28)

## V15.3.4

Verify that all proxying and middleware components transfer the user's original IP address correctly using trusted data fields that cannot be manipulated by the end user, and the application and web server use this correct value for logging and security decisions such as rate limiting, taking into account that even the original IP address may not be reliable due to dynamic IPs, VPNs, or corporate firewalls.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [137](/taxonomy/capec-3.9/137), [28](/taxonomy/capec-3.9/28)

## V15.3.5

Verify that the application explicitly ensures that variables are of the correct type and performs strict equality and comparator operations. This is to avoid type juggling or type confusion vulnerabilities caused by the application code making an assumption about a variable type.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [137](/taxonomy/capec-3.9/137), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [19](/taxonomy/capec-3.9/19), [261](/taxonomy/capec-3.9/261), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28)

## V15.3.6

Verify that JavaScript code is written in a way that prevents prototype pollution, for example, by using Set() or Map() instead of object literals.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [137](/taxonomy/capec-3.9/137), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [160](/taxonomy/capec-3.9/160), [19](/taxonomy/capec-3.9/19), [261](/taxonomy/capec-3.9/261), [267](/taxonomy/capec-3.9/267), [28](/taxonomy/capec-3.9/28)

## V15.3.7

Verify that the application has defenses against HTTP parameter pollution attacks, particularly if the application framework makes no distinction about the source of request parameters (query string, body parameters, cookies, or header fields).

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [113](/taxonomy/capec-3.9/113), [137](/taxonomy/capec-3.9/137), [162](/taxonomy/capec-3.9/162), [19](/taxonomy/capec-3.9/19), [261](/taxonomy/capec-3.9/261), [28](/taxonomy/capec-3.9/28), [39](/taxonomy/capec-3.9/39)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
