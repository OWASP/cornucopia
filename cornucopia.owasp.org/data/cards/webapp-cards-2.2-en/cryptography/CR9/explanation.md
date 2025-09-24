## Scenario: Andy's Bypassing of Weak Custom Cryptographic Functions

Consider a situation where Andy bypasses crucial cryptographic functions like random number generation, GUID generation, hashing, and encryption because they are self-built and inadequately secure. This issue arises from:

1. **Self-Built Cryptographic Functions:** The application relies on custom-developed cryptographic functions, which may not meet industry security standards.

2. **Weaknesses in Custom Algorithms:** These self-built functions are not as robust or tested as established cryptographic standards, making them vulnerable to exploitation.

### Example

Andy targets a system that uses a custom-built encryption algorithm and a self-developed function for generating random numbers. He identifies weaknesses in these algorithms, such as predictable patterns in random number generation and flaws in the encryption process. Leveraging these vulnerabilities, Andy is able to predict supposedly random values and decrypt sensitive data, bypassing the intended security measures of the system.

## Threat Modeling

### STRIDE

The primary applicable STRIDE categories for this scenario is **Information Disclosure** or **Tampering** depending on the context.

- Andy may be able to undermine the integrity of the system’s protections (random numbers, GUIDs, hashing, encryption). By bypassing or breaking them, he can alter outcomes (predictable GUIDs, weakened encryption, manipulated “random” values). This is a failure of integrity which makes the primary impact: **Tampering**.
- Andy’s bypass of weak/random crypto may give him a "backdoor" in encrypted communication that allow him to see what information is being sent. In that case the main harm is loss of confidentiality, primary impact: **Information Disclosure**.

### What can go Wrong?

Reliance on weak, custom-built cryptographic functions can lead to compromised data security, unauthorized access, and potential breaches of sensitive information.

### What are you going to do about it?

- Replace custom cryptographic functions with well-established, industry-standard algorithms and libraries that have been rigorously tested and proven secure.
- Conduct regular security audits and reviews of cryptographic implementations to ensure they are strong and effective.
- Avoid developing in-house cryptographic solutions unless absolutely necessary and ensure they are developed by experts in cryptography.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
