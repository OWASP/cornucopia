# CAPEC™ 100: Overflow Buffers

## Description

Buffer Overflow attacks target improper or missing bounds checking on buffer operations, typically triggered by input injected by an adversary. As a consequence, an adversary is able to write past the boundaries of allocated buffer regions in memory, causing a program crash or potentially redirection of execution as per the adversaries' choice.

Source: [CAPEC™ 100](https://capec.mitre.org/data/definitions/100.html)

## Related ASVS Requirements

ASVS (5.0): [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.5.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.2), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3), [4.2.5](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.5), [4.3.1](/taxonomy/asvs-5.0/04-api-and-web-service/03-graphql#V4.3.1)
