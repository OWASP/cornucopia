## Scenario: Kyle's Bypassing of Non-Secure Cryptographic Failures

Envision a scenario where Kyle exploits cryptographic systems that default to an unprotected state when they fail. This vulnerability arises from:

1. **Non-Secure Default in Failure Scenarios:** In case of a failure in the cryptographic process, the system defaults to allowing access or processing data without encryption, rather than ensuring protection.

### Example

Kyle targets an application that handles sensitive data encryption. He observes that when there’s a failure in the encryption process, perhaps due to configuration errors or system issues, the application continues to process and transmit data in an unencrypted state. Exploiting this, Kyle induces failures in the cryptographic system, causing the application to revert to its non-secure default state. This allows him to access sensitive data that should have been encrypted.

## Threat Modeling

### STRIDE

The applicable STRIDE category for this scenario is **Information Disclosure** or **Tampering** depending on the context.

Kyle may be able to access sensitive data because the cryptographic controls fail insecurely (defaulting to unprotected).
The main impact than is that confidential information is exposed, rather than modified (Tampering) or misused to gain higher privileges (Elevation of Privilege), but if the scenario involves cryptographic integrity mechanisms, like digital signatures or message authentication codes (MACs), then a failure could allow Kyle to modify data undetected. In that case, the primary impact would be **Tampering** rather than **Information Disclosure**.


### What can go Wrong?

Such a vulnerability can lead to data exposure and breaches, as it allows sensitive information to be processed or transmitted without the intended cryptographic protection.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Design cryptographic systems to fail securely, ensuring that in the event of a failure, data remains protected or access is restricted.
2. Implement robust error handling that maintains security standards even when cryptographic processes encounter issues.
3. Regularly test and audit cryptographic systems to ensure they respond securely to failures and do not expose sensitive data.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
