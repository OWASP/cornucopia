# CAPEC™ 201: Serialized Data External Linking

## Description

An adversary creates a serialized data file (e.g. XML, YAML, etc...) that contains an external data reference. Because serialized data parsers may not validate documents with external references, there may be no checks on the nature of the reference in the external data. This can allow an adversary to open arbitrary files or connections, which may further lead to the adversary gaining access to information on the system that they would normally be unable to obtain.

Source: [CAPEC™ 201](https://capec.mitre.org/data/definitions/201.html)

## Related ASVS Requirements

ASVS (5.0): [1.3.6](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.6), [1.3.8](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.8), [1.5.1](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.1), [1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2)
