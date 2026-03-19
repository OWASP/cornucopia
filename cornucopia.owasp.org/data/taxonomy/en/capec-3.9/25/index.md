# CAPEC™ 25: Forced Deadlock

## Description

The adversary triggers and exploits a deadlock condition in the target software to cause a denial of service. A deadlock can occur when two or more competing actions are waiting for each other to finish, and thus neither ever does. Deadlock conditions can be difficult to detect.

Source: [CAPEC™ 25](https://capec.mitre.org/data/definitions/25.html)

## Related ASVS Requirements

ASVS (5.0): [1.4.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.1), [1.4.2](/taxonomy/asvs-5.0/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.2), [15.4.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.3), [15.4.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.4), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.5.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.2), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3), [2.3.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.2), [4.2.5](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.5)
