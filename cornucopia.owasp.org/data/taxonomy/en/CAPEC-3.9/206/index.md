# CAPEC™ 206: Signing Malicious Code

## Description

The adversary extracts credentials used for code signing from a production environment and then uses these credentials to sign malicious content with the developer's key. Many developers use signing keys to sign code or hashes of code. When users or applications verify the signatures are accurate they are led to believe that the code came from the owner of the signing key and that the code has not been modified since the signature was applied. If the adversary has extracted the signing credentials then they can use those credentials to sign their own code bundles. Users or tools that verify the signatures attached to the code will likely assume the code came from the legitimate developer and install or run the code, effectively allowing the adversary to execute arbitrary code on the victim's computer. This differs from CAPEC-673, because the adversary is performing the code signing.

Source: [CAPEC™ 206](https://capec.mitre.org/data/definitions/206.html)

## Related ASVS Requirements

ASVS (5.0): [13.3.1](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.1), [13.3.2](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.2), [13.3.3](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.3), [16.3.1](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.1), [16.3.2](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.2), [16.3.3](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.3), [16.3.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/03-security-events#V16.3.4)
