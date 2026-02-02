# CAPEC™ 475: Signature Spoofing by Improper Validation

## Description

An adversary exploits a cryptographic weakness in the signature verification algorithm implementation to generate a valid signature without knowing the key.

Source: [CAPEC™ 475](https://capec.mitre.org/data/definitions/475.html)

## Related ASVS Requirements

ASVS (5.0): [11.3.3](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.3), [11.3.5](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.5), [11.4.3](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.3), [14.2.4](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.4), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [2.2.1](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.1), [2.2.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/02-input-validation#V2.2.2), [3.6.1](/taxonomy/asvs-5.0/03-web-frontend-security/06-external-resource-integrity#V3.6.1), [4.1.5](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.5), [6.8.2](/taxonomy/asvs-5.0/06-authentication/08-authentication-with-an-identity-provider#V6.8.2), [9.1.1](/taxonomy/asvs-5.0/09-self-contained-tokens/01-token-source-and-integrity#V9.1.1), [9.1.2](/taxonomy/asvs-5.0/09-self-contained-tokens/01-token-source-and-integrity#V9.1.2), [9.1.3](/taxonomy/asvs-5.0/09-self-contained-tokens/01-token-source-and-integrity#V9.1.3)
