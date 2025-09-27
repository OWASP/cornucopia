## Scenario: Kyun’s Access to Obfuscated Data

Imagine a scenario where Kyun accesses sensitive data that has been obfuscated but not securely encrypted. This occurs due to:

1. **Reliance on Obfuscation:** The system uses obfuscation methods, which merely disguise data, instead of employing robust cryptographic functions for security.

2. **Lack of Approved Cryptographic Standards:** The absence of standard, approved cryptographic techniques leads to weaker data protection.

### Example

Kyun targets a system where critical data, such as passwords and user details, are merely obfuscated — for instance, using basic encoding techniques like Base64 — rather than being encrypted. Kyun deciphers this obfuscated data with ease, as these methods do not provide any significant barrier against someone with technical knowledge. The lack of strong, approved cryptographic functions means that what appeared to be protected data is easily accessible to Kyun.

## Threat Modeling

### STRIDE

The applicable STRIDE category for this scenario is **Information Disclosure**.

Kyun is able to access sensitive data (passwords, user details) that was not properly protected.
The data was only obfuscated, not securely encrypted, so confidential information is exposed to an attacker.

### What can go Wrong?

Such practices can lead to unauthorized data access and breaches, as obfuscation alone is insufficient to protect against determined attackers.

### What are you going to do about it?

1. Replace obfuscation techniques with approved cryptographic functions for data protection.
2. Ensure the implementation of industry-standard encryption algorithms to secure sensitive data.
3. Regularly review and update cryptographic practices to align with current security standards and best practices.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
