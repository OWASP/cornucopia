# CAPEC™ 461: Web Services API Signature Forgery Leveraging Hash Function Extension Weakness

## Description

An adversary utilizes a hash function extension/padding weakness, to modify the parameters passed to the web service requesting authentication by generating their own call in order to generate a legitimate signature hash (as described in the notes), without knowledge of the secret token sometimes provided by the web service.

Source: [CAPEC™ 461](https://capec.mitre.org/data/definitions/461.html)

## Related ASVS Requirements

ASVS (5.0): [11.2.2](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.2), [11.2.5](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.5), [11.3.1](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.1), [11.3.2](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.2), [11.3.3](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.3), [11.3.5](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.5), [11.4.1](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.1), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [16.5.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.3)
