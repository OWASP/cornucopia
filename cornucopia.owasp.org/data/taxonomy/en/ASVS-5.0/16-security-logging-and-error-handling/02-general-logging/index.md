# General Logging

## V16.2.1

Verify that each log entry includes necessary metadata (such as when, where, who, what) that would allow for a detailed investigation of the timeline when an event happens.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151/index.md), [21](/taxonomy/capec-3.9/21/index.md), [268](/taxonomy/capec-3.9/268/index.md), [49](/taxonomy/capec-3.9/49/index.md), [50](/taxonomy/capec-3.9/50/index.md), [600](/taxonomy/capec-3.9/600/index.md)

## V16.2.2

Verify that time sources for all logging components are synchronized, and that timestamps in security event metadata use UTC or include an explicit time zone offset. UTC is recommended to ensure consistency across distributed systems and to prevent confusion during daylight saving time transitions.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151/index.md), [21](/taxonomy/capec-3.9/21/index.md), [268](/taxonomy/capec-3.9/268/index.md), [49](/taxonomy/capec-3.9/49/index.md), [50](/taxonomy/capec-3.9/50/index.md), [600](/taxonomy/capec-3.9/600/index.md)

## V16.2.3

Verify that the application only stores or broadcasts logs to the files and services that are documented in the log inventory.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151/index.md), [21](/taxonomy/capec-3.9/21/index.md), [268](/taxonomy/capec-3.9/268/index.md), [49](/taxonomy/capec-3.9/49/index.md), [50](/taxonomy/capec-3.9/50/index.md), [600](/taxonomy/capec-3.9/600/index.md)

## V16.2.4

Verify that logs can be read and correlated by the log processor that is in use, preferably by using a common logging format.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [151](/taxonomy/capec-3.9/151/index.md), [21](/taxonomy/capec-3.9/21/index.md), [268](/taxonomy/capec-3.9/268/index.md), [49](/taxonomy/capec-3.9/49/index.md), [50](/taxonomy/capec-3.9/50/index.md), [600](/taxonomy/capec-3.9/600/index.md)

## V16.2.5

Verify that when logging sensitive data, the application enforces logging based on the data's protection level. For example, it may not be allowed to log certain data, such as credentials or payment details. Other data, such as session tokens, may only be logged by being hashed or masked, either in full or partially.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [116](/taxonomy/capec-3.9/116/index.md), [151](/taxonomy/capec-3.9/151/index.md), [155](/taxonomy/capec-3.9/155/index.md), [169](/taxonomy/capec-3.9/169/index.md), [21](/taxonomy/capec-3.9/21/index.md), [215](/taxonomy/capec-3.9/215/index.md), [268](/taxonomy/capec-3.9/268/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [49](/taxonomy/capec-3.9/49/index.md), [50](/taxonomy/capec-3.9/50/index.md), [54](/taxonomy/capec-3.9/54/index.md), [593](/taxonomy/capec-3.9/593/index.md), [600](/taxonomy/capec-3.9/600/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
