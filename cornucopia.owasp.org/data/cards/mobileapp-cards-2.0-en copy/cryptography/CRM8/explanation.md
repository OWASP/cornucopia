## Scenario: Ash can break the cryptography because it is not strong enough according to what is recommended or the perceived effort of a potential attacker

### Example

Ash protects a decade of medical scans with a cipher that was fashionable when flip phones were exciting. A modern workstation cracks it during the time Ash spends choosing a sandwich, then prints the scans on both sides to save paper.

Cryptography must match current recommendations and the attacker’s realistic resources. Algorithms, key sizes, and modes that no longer provide adequate work factors leave protected data within practical reach.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Ash can break the cryptography because it is not strong enough according to what is recommended or the perceived effort of a potential attacker.

- **MAS-THREAT-0013:** Attackers can predict or reproduce improperly generated cryptographic keys.
- **MAS-THREAT-0007:** Attackers can decrypt or forge improperly encrypted data.
- **MAS-THREAT-0008:** Attackers can forge or replay data that passes hash-based integrity or authenticity checks.

- **MAS-ATTACK-0018:** Brute-forcing cryptographic material generated with insufficient length.
- **MAS-ATTACK-0019:** Recovering or guessing the seed used by the generator to reproduce its output.
- **MAS-ATTACK-0020:** Intercepting cryptographic keys exported in plaintext.
- **MAS-ATTACK-0021:** Performing cryptanalysis of broken algorithms, modes, or parameters.
- **MAS-ATTACK-0022:** Exploiting predictable or reused IVs or nonces to detect patterns or recover plaintext.
- **MAS-ATTACK-0023:** Exploiting padding oracles exposed through observable error signals or timing differences.
- **MAS-ATTACK-0028:** Crafting collisions or second preimages for broken hash functions.

### What can go wrong?

If Ash can break the cryptography because it is not strong enough according to what is recommended or the perceived effort of a potential attacker, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Brute-forcing cryptographic material generated with insufficient length. Also, Recovering or guessing the seed used by the generator to reproduce its output. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0013 — Improper Cryptographic Key Generation: This weakness occurs when cryptographic keys are generated with insufficient length, insufficient entropy, or otherwise flawed generation processes, weakening every protection built on top of them.
- MASWE-0007 — Improper Encryption: This weakness occurs when encryption is implemented with broken algorithms, insecure modes or parameters, or non-cryptographic techniques, leaving the protected data recoverable or forgeable without the key.
- MASWE-0008 — Improper Hashing: This weakness occurs when a broken or unsuitable hash function is used in a security-sensitive context, such as integrity checks, digital signatures, or certificate fingerprints.

### What are we going to do about it?

Choose currently approved algorithms, modes, and key lengths that match the attacker's expected effort, and remove legacy or undersized alternatives; confirm the effective configuration through static review and runtime cryptography tests.


Mapped MASTG tests:

- MASTG-TEST-0208 — Insufficient Key Sizes: In this test case, we will look for the use insufficient key sizes in Android apps. To do this, we need to focus on the cryptographic frameworks and libraries that are available in Android and the methods that are used to generate,...
- MASTG-TEST-0209 — Insufficient Key Sizes: In this test case, we will look for the use insufficient key sizes in iOS apps. To do this, we need to focus on APIs from cryptographic frameworks and libraries that are available in iOS and the methods that are used to generate...
- MASTG-TEST-0210 — Broken Symmetric Encryption Algorithms: To test for the use of broken encryption algorithms in iOS apps, we need to focus on APIs from cryptographic frameworks and libraries that are used to perform encryption and decryption operations.
- MASTG-TEST-0211 — Broken Hashing Algorithms: To test for the use of broken hashing algorithms in iOS apps, we need to focus on APIs from cryptographic frameworks and libraries that are used to perform hashing operations.
- MASTG-TEST-0221 — Broken Symmetric Encryption Algorithms: To test for the use of broken encryption algorithms in Android apps, we need to focus on methods from cryptographic frameworks and libraries that are used to perform encryption and decryption operations.
- MASTG-TEST-0232 — Broken Symmetric Encryption Modes: To test for the use of broken encryption modes in Android apps, we should focus on methods in cryptographic frameworks and libraries used to configure and apply encryption modes.
- MASTG-TEST-0312 — References to Explicit Security Provider in Cryptographic APIs: Android cryptography APIs based on the Java Cryptography Architecture (JCA) allow developers to specify a security provider when calling `getInstance` methods. However, explicitly specifying a provider can cause security issues and...
- MASTG-TEST-0317 — Broken Symmetric Encryption Modes: This test focuses on broken symmetric encryption modes such as ECB (Electronic Codebook)).
- MASTG-TEST-0350 — Runtime Use of Broken Symmetric Encryption Modes: If the app configures cryptographic operations with broken encryption modes at runtime, sensitive data can be exposed to pattern leakage and other cryptographic weaknesses. This test checks whether the running app sets insecure block...

Mapped MASTG best practices:

- MASTG-BEST-0009 — Use Secure Encryption Algorithms: Replace insecure encryption algorithms with secure ones such as AES-256 (preferably in GCM mode) or Chacha20.
- MASTG-BEST-0005 — Use Secure Encryption Modes: Replace insecure encryption modes with secure block cipher modes such as AES-GCM or AES-CCM which are authenticated encryption modes that provide confidentiality, integrity, and authenticity.
- MASTG-BEST-0020 — Update the GMS Security Provider: Android devices vary widely in OS version and update frequency. Relying solely on platform-level security can leave apps exposed to outdated SSL/TLS implementations and known vulnerabilities.

Mapped MASTG knowledge:

- MASTG-KNOW-0012 — Key Generation: The Android SDK allows you to specify how a key should be generated, and under which circumstances it can be used. Android 6.0 (API level 23) introduced the `KeyGenParameterSpec` class that can be used to ensure the correct key usage in...
- MASTG-KNOW-0011 — Security Provider: Android relies on a security provider via the `java.security.Provider` class to implement Java Security services and provide SSL/TLS-based connections. These providers are crucial to ensure secure network communications and secure other...
