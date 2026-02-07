# CAPEC™ 442: Infected Software

## Description

An adversary adds malicious logic, often in the form of a computer virus, to otherwise benign software. This logic is often hidden from the user of the software and works behind the scenes to achieve negative impacts. Many times, the malicious logic is inserted into empty space between legitimate code, and is then called when the software is executed. This pattern of attack focuses on software already fielded and used in operation as opposed to software that is still under development and part of the supply chain.

Source: [CAPEC™ 442](https://capec.mitre.org/data/definitions/442.html)

## Related ASVS Requirements

ASVS (5.0): [11.3.3](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.3), [11.4.3](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.3), [14.2.4](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.4), [15.1.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.1), [15.1.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.2), [15.1.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.4), [15.1.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.5), [15.2.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.1), [15.2.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.4), [15.2.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.5), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [4.1.5](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.5), [6.7.1](/taxonomy/asvs-5.0/06-authentication/07-cryptographic-authentication-mechanism#V6.7.1)
