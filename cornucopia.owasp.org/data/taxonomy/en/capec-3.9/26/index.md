# CAPEC™ 26: Leveraging Race Conditions

## Description

The adversary targets a race condition occurring when multiple processes access and manipulate the same resource concurrently, and the outcome of the execution depends on the particular order in which the access takes place. The adversary can leverage a race condition by "running the race", modifying the resource and modifying the normal execution flow. For instance, a race condition can occur while accessing a file: the adversary can trick the system by replacing the original file with their version and cause the system to read the malicious file.

Source: [CAPEC™ 26](https://capec.mitre.org/data/definitions/26.html)

## Related ASVS Requirements

ASVS (5.0): [15.4.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.1), [15.4.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3), [2.3.4](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.4), [2.4.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.2)
