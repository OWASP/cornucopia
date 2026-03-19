# Random Values

## V11.5.1

Verify that all random numbers and strings which are intended to be non-guessable must be generated using a cryptographically secure pseudo-random number generator (CSPRNG) and have at least 128 bits of entropy. Note that UUIDs do not respect this condition.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [272](/taxonomy/capec-3.9/272), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## V11.5.2

Verify that the random number generation mechanism in use is designed to work securely, even under heavy demand.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [272](/taxonomy/capec-3.9/272), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
