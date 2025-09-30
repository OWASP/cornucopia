## Scenario: Susanna’s Ability to Break Weak Cryptography

Envision a scenario where Susanna, an attacker, manages to break the cryptographic protections in use because they are not sufficiently robust. This issue arises from:

1. **Inadequate Strength for Required Protection:** The cryptography level does not match the sensitivity or importance of the data it is protecting.

2. **Underestimation of Attacker Capabilities:** The cryptographic strength is not sufficient to withstand the efforts of determined attackers.

### Example

Susanna targets an application storing highly sensitive user data, protected by outdated cryptographic algorithms. She dedicates significant resources to cracking these cryptographic protections. Due to the use of older, weaker cryptographic methods that no longer meet current security standards, Susanna successfully decrypts the data, accessing confidential information. The cryptography used was not strong enough to withstand the level of effort and resources she was willing to invest.

## Threat Modeling

### STRIDE

The primary applicable STRIDE categories for this scenario is **Information Disclosure** or **Tampering** depending on the context.

1. STRIDE’s **Information Disclosure** covers unauthorized exposure of sensitive information — which is what occurs when encryption is insufficient and an attacker can decrypt data. Breaking weak or outdated cryptography lets an attacker read confidential data that was supposed to be protected (passwords, PII, cardholder data, secrets).
2. If the cryptographic primitive is providing integrity (signatures or MACs) and an attacker is able to break or bypass that protection so they can alter data without detection, then the primary STRIDE impact is **Tampering**.

### What can go wrong?

Using cryptography that is not sufficiently strong for the required level of protection can lead to data breaches, unauthorized access, and exposure of sensitive information.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

The choice of cryptographic algorithm, its configuration, and key length will not be the same for all deployments. Appropriate selection needs to be based on risk.

1. Assess the sensitivity and value of the data being protected and ensure the strength of the cryptographic measures is adequate to provide the necessary level of security.
2. Regularly update and upgrade cryptographic algorithms and practices to align with current security standards and to counteract evolving threats.
3. Monitor developments in cryptography and cybersecurity to anticipate and prepare for potential efforts by attackers.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
