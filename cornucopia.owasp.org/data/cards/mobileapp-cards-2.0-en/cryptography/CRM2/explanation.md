## Scenario: Lesego can compromise cryptographic operations and resources because keys are reused for multiple purposes, or not used according to the purpose for which they were created

### Example

Lesego labels the keys to a campsite, locker, and canoe shed with one master key because the ring looks wonderfully organized. When a stranger copies the shed key, it opens the locker and the ranger’s “emergency snacks” cabinet too.

Cryptographic keys need separate purposes and appropriate access rules. Reusing one key across unrelated operations lets compromise in one context unlock or forge data in another.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Lesego can compromise cryptographic operations and resources because keys are reused for multiple purposes, or not used according to the purpose for which they were created.

- **MAS-THREAT-0007:** Attackers can decrypt or forge improperly encrypted data.

- **MAS-ATTACK-0018:** Brute-forcing cryptographic material generated with insufficient length.
- **MAS-ATTACK-0021:** Performing cryptanalysis of broken algorithms, modes, or parameters.
- **MAS-ATTACK-0022:** Exploiting predictable or reused IVs or nonces to detect patterns or recover plaintext.
- **MAS-ATTACK-0023:** Exploiting padding oracles exposed through observable error signals or timing differences.

### What can go wrong?

If Lesego can compromise cryptographic operations and resources because keys are reused for multiple purposes, or not used according to the purpose for which they were created, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Brute-forcing cryptographic material generated with insufficient length. Also, Performing cryptanalysis of broken algorithms, modes, or parameters. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0007 — Improper Encryption: This weakness occurs when encryption is implemented with broken algorithms, insecure modes or parameters, or non-cryptographic techniques, leaving the protected data recoverable or forgeable without the key.

### What are we going to do about it?

Give each cryptographic key one declared purpose and enforce it with platform key-generation parameters such as Android KeyGenParameterSpec; use separate keys for encryption, signing, and wrapping, then test both key references and runtime operations.


Mapped MASTG tests:

- MASTG-TEST-0307 — References to Asymmetric Key Pairs Used For Multiple Purposes: According to section "5.2 Key Usage" of NIST SP 800-57 part 1 revision 5, cryptographic keys should be assigned a specific purpose and used only for that purpose (e.g., encryption, integrity authentication, key wrapping, random bit...
- MASTG-TEST-0308 — Runtime Use of Asymmetric Key Pairs Used For Multiple Purposes: This test is the dynamic counterpart to @MASTG-TEST-0307, but it focuses on intercepting cryptographic operations rather than generating keys with multiple purposes.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0012 — Key Generation: The Android SDK allows you to specify how a key should be generated, and under which circumstances it can be used. Android 6.0 (API level 23) introduced the `KeyGenParameterSpec` class that can be used to ensure the correct key usage in...
