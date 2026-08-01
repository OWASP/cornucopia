# CAPEC™ 68: Subvert Code-signing Facilities

## Description

Many languages use code signing facilities to vouch for code's identity and to thus tie code to its assigned privileges within an environment. Subverting this mechanism can be instrumental in an attacker escalating privilege. Any means of subverting the way that a virtual machine enforces code signing classifies for this style of attack.

Source: [CAPEC™ 68](https://capec.mitre.org/data/definitions/68.html)

## Related ASVS Requirements

ASVS (5.0): [11.3.3](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.3), [11.4.1](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.1), [11.4.3](/taxonomy/asvs-5.0/11-cryptography/04-hashing-and-hash-based-functions#V11.4.3), [11.6.1](/taxonomy/asvs-5.0/11-cryptography/06-public-key-cryptography#V11.6.1), [11.6.2](/taxonomy/asvs-5.0/11-cryptography/06-public-key-cryptography#V11.6.2), [13.3.1](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.1), [13.3.2](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.2), [13.3.3](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.3), [14.2.4](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.4), [15.2.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.5), [16.3.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.1), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4), [4.1.5](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.5), [6.3.3](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.3), [6.7.1](/taxonomy/asvs-5.0/06-authentication/07-cryptographic-authentication-mechanism#V6.7.1)
