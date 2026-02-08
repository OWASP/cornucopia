# Configuration Documentation

## V13.1.1

Verify that all communication needs for the application are documented. This must include external services which the application relies upon and cases where an end user might be able to provide an external location to which the application will then connect.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [154](/taxonomy/capec-3.9/154/index.md), [176](/taxonomy/capec-3.9/176/index.md), [240](/taxonomy/capec-3.9/240/index.md), [481](/taxonomy/capec-3.9/481/index.md)

## V13.1.2

Verify that for each service the application uses, the documentation defines the maximum number of concurrent connections (e.g., connection pool limits) and how the application behaves when that limit is reached, including any fallback or recovery mechanisms, to prevent denial of service conditions.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [125](/taxonomy/capec-3.9/125/index.md), [227](/taxonomy/capec-3.9/227/index.md)

## V13.1.3

Verify that the application documentation defines resourcemanagement strategies for every external system or service it uses (e.g., databases, file handles, threads, HTTP connections). This should include resourcerelease procedures, timeout settings, failure handling, and where retry logic is implemented, specifying retry limits, delays, and backoff algorithms. For synchronous HTTP requestresponse operations it should mandate short timeouts and either disable retries or strictly limit retries to prevent cascading delays and resource exhaustion.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [125](/taxonomy/capec-3.9/125/index.md), [227](/taxonomy/capec-3.9/227/index.md), [603](/taxonomy/capec-3.9/603/index.md), [607](/taxonomy/capec-3.9/607/index.md)

## V13.1.4

Verify that the application's documentation defines the secrets that are critical for the security of the application and a schedule for rotating them, based on the organization's threat model and business requirements.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [155](/taxonomy/capec-3.9/155/index.md), [204](/taxonomy/capec-3.9/204/index.md), [37](/taxonomy/capec-3.9/37/index.md), [474](/taxonomy/capec-3.9/474/index.md), [548](/taxonomy/capec-3.9/548/index.md), [57](/taxonomy/capec-3.9/57/index.md), [639](/taxonomy/capec-3.9/639/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
