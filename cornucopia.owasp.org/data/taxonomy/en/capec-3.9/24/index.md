# CAPEC™ 24: Filter Failure through Buffer Overflow

## Description

In this attack, the idea is to cause an active filter to fail by causing an oversized transaction. An attacker may try to feed overly long input strings to the program in an attempt to overwhelm the filter (by causing a buffer overflow) and hoping that the filter does not fail securely (i.e. the user input is let into the system unfiltered).

Source: [CAPEC™ 24](https://capec.mitre.org/data/definitions/24.html)

## Related ASVS Requirements

ASVS (5.0): [11.2.5](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.5), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.1), [16.5.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.2), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3), [16.5.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.4)
