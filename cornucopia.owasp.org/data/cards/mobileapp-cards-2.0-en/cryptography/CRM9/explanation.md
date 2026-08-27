## Scenario: Ramsey can access protected sensitive data because cryptographic configuration (e.g. algorithm, mode, IV, nonce, or provider) is weak or incorrectly used

### Example

Ramsey’s ticket app uses the same nonce for every encrypted boarding pass. An eavesdropper compares two passes and learns enough about their shared structure to swap Ramsey’s destination for “Platform 9¾.”

Secure algorithms still fail when configured incorrectly. Correct modes, unique IVs or nonces, and vetted providers prevent configuration mistakes from exposing or corrupting ciphertext.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Ramsey can access protected sensitive data because cryptographic configuration (e.g. algorithm, mode, IV, nonce, or provider) is weak or incorrectly used.

- **MAS-THREAT-0007:** Attackers can decrypt or forge improperly encrypted data.

- **MAS-ATTACK-0018:** Brute-forcing cryptographic material generated with insufficient length.
- **MAS-ATTACK-0021:** Performing cryptanalysis of broken algorithms, modes, or parameters.
- **MAS-ATTACK-0022:** Exploiting predictable or reused IVs or nonces to detect patterns or recover plaintext.
- **MAS-ATTACK-0023:** Exploiting padding oracles exposed through observable error signals or timing differences.

### What can go wrong?

If Ramsey can access protected sensitive data because cryptographic configuration (e.g. algorithm, mode, IV, nonce, or provider) is weak or incorrectly used, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Brute-forcing cryptographic material generated with insufficient length. Also, Performing cryptanalysis of broken algorithms, modes, or parameters. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0007 — Improper Encryption: This weakness occurs when encryption is implemented with broken algorithms, insecure modes or parameters, or non-cryptographic techniques, leaving the protected data recoverable or forgeable without the key.

### What are we going to do about it?

Use an approved provider and AEAD mode with securely generated, non-reused IVs or nonces, authenticated associated data where needed, and constant-time verification; test the actual algorithm, mode, parameters, and error timing.


Mapped MASTG tests:

- MASTG-TEST-0210 — Broken Symmetric Encryption Algorithms: To test for the use of broken encryption algorithms in iOS apps, we need to focus on APIs from cryptographic frameworks and libraries that are used to perform encryption and decryption operations.
- MASTG-TEST-0221 — Broken Symmetric Encryption Algorithms: To test for the use of broken encryption algorithms in Android apps, we need to focus on methods from cryptographic frameworks and libraries that are used to perform encryption and decryption operations.
- MASTG-TEST-0232 — Broken Symmetric Encryption Modes: To test for the use of broken encryption modes in Android apps, we should focus on methods in cryptographic frameworks and libraries used to configure and apply encryption modes.
- MASTG-TEST-0309 — References to Reused Initialization Vectors in Symmetric Encryption: The source provides the mapped security guidance for this control.
- MASTG-TEST-0310 — Runtime Use of Reused Initialization Vectors in Symmetric Encryption: The source provides the mapped security guidance for this control.
- MASTG-TEST-0312 — References to Explicit Security Provider in Cryptographic APIs: Android cryptography APIs based on the Java Cryptography Architecture (JCA) allow developers to specify a security provider when calling `getInstance` methods. However, explicitly specifying a provider can cause security issues and...
- MASTG-TEST-0317 — Broken Symmetric Encryption Modes: This test focuses on broken symmetric encryption modes such as ECB (Electronic Codebook)).
- MASTG-TEST-0350 — Runtime Use of Broken Symmetric Encryption Modes: If the app configures cryptographic operations with broken encryption modes at runtime, sensitive data can be exposed to pattern leakage and other cryptographic weaknesses. This test checks whether the running app sets insecure block...

Mapped MASTG best practices:

- MASTG-BEST-0009 — Use Secure Encryption Algorithms: Replace insecure encryption algorithms with secure ones such as AES-256 (preferably in GCM mode) or Chacha20.
- MASTG-BEST-0005 — Use Secure Encryption Modes: Replace insecure encryption modes with secure block cipher modes such as AES-GCM or AES-CCM which are authenticated encryption modes that provide confidentiality, integrity, and authenticity.
- MASTG-BEST-0020 — Update the GMS Security Provider: Android devices vary widely in OS version and update frequency. Relying solely on platform-level security can leave apps exposed to outdated SSL/TLS implementations and known vulnerabilities.

Mapped MASTG knowledge:

- MASTG-KNOW-0011 — Security Provider: Android relies on a security provider via the `java.security.Provider` class to implement Java Security services and provide SSL/TLS-based connections. These providers are crucial to ensure secure network communications and secure other...
