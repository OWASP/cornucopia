## Scenario: Emery can access data because it has been obfuscated rather than using an approved cryptographic function

### Example

Emery hides a house key by writing its location in a simple letter-shift cipher on the garden shed. A curious neighbor decodes it during lunch and finds not only the key but Emery’s legendary emergency biscuit tin.

Obfuscation only makes data look unfamiliar; it does not provide cryptographic confidentiality. Sensitive app data needs an approved encryption function with protected keys, not a puzzle that anyone can solve.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure** in STRIDE. The named condition is: Emery can access data because it has been obfuscated rather than using an approved cryptographic function.

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

If Emery can access data because it has been obfuscated rather than using an approved cryptographic function, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Brute-forcing cryptographic material generated with insufficient length. Also, Recovering or guessing the seed used by the generator to reproduce its output. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0013 — Improper Cryptographic Key Generation: This weakness occurs when cryptographic keys are generated with insufficient length, insufficient entropy, or otherwise flawed generation processes, weakening every protection built on top of them.
- MASWE-0007 — Improper Encryption: This weakness occurs when encryption is implemented with broken algorithms, insecure modes or parameters, or non-cryptographic techniques, leaving the protected data recoverable or forgeable without the key.
- MASWE-0008 — Improper Hashing: This weakness occurs when a broken or unsuitable hash function is used in a security-sensitive context, such as integrity checks, digital signatures, or certificate fingerprints.

### What are we going to do about it?

Replace obfuscation or encoding with an approved primitive such as AES-GCM or ChaCha20-Poly1305, and use a vetted hash for integrity; test that protected data cannot be recovered or forged without the key.


Mapped MASTG tests:

- MASTG-TEST-0209 — Insufficient Key Sizes: In this test case, we will look for the use insufficient key sizes in iOS apps. To do this, we need to focus on APIs from cryptographic frameworks and libraries that are available in iOS and the methods that are used to generate...
- MASTG-TEST-0210 — Broken Symmetric Encryption Algorithms: To test for the use of broken encryption algorithms in iOS apps, we need to focus on APIs from cryptographic frameworks and libraries that are used to perform encryption and decryption operations.
- MASTG-TEST-0211 — Broken Hashing Algorithms: To test for the use of broken hashing algorithms in iOS apps, we need to focus on APIs from cryptographic frameworks and libraries that are used to perform hashing operations.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0111 — Obfuscation: Obfuscation is the process of transforming code and data to make it more difficult to comprehend (and sometimes even difficult to disassemble). It is usually an integral part of the software protection scheme. Obfuscation isn't...
