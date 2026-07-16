## Scenario: Hassan can extract or modify sensitive data because functions for storage and/or encryption are weak, deprecated, or used incorrectly

Consider a scenario where Hassan finds the app uses AES-CBC with a static IV. The IV is always the same 16-byte value, copied from a constant in the code. Two plaintexts encrypted with the same key and same IV produce ciphertext blocks that are identical for identical plaintext prefixes — allowing an attacker who can observe multiple ciphertexts to infer information about the plaintexts. The developer had set the IV to all zeros "for simplicity."

1. A static IV with AES-CBC creates a deterministic cipher; identical plaintext prefixes produce identical ciphertext blocks.
2. Using an IV that is shorter than the required 16 bytes, or zero-padded, reduces the effective randomness.
3. Using `AES/ECB/PKCS5Padding` instead of `AES/GCM/NoPadding` as a "simpler" alternative loses integrity protection and leaks plaintext structure.

### Example

Hassan captures 100 ciphertext blocks from different users' encrypted profiles. Each profile starts with `{"name":"`. Because the IV is static, the first ciphertext block is always the AES-CBC encryption of `{"name":"` XOR `IV`. Since `IV` is constant, the first ciphertext block is the same for all users with profiles starting with the same 16 bytes. Hassan uses this to identify accounts with the same name prefix — and then confirms specific values by testing known plaintexts. The AES implementation was correct. Its use was not.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Incorrect use of cryptographic functions — even correct algorithms used with incorrect parameters — can expose plaintext structure, enable known-plaintext attacks, or make the encryption deterministic and therefore guessable.

### What can go wrong?

- Static IV enables determination of plaintext structure from ciphertext patterns.
- ECB mode leaks block-level plaintext repetitions.
- Re-used nonces in GCM mode expose the authentication key, breaking both confidentiality and integrity.
- PKCS#1 v1.5 RSA padding is vulnerable to Bleichenbacher's oracle attack.

### What are we going to do about it?

- Always generate a fresh random IV/nonce for each encryption operation: `SecureRandom().nextBytes(iv)`.
- Never reuse a nonce with the same GCM key.
- Store the IV alongside the ciphertext for decryption (the IV is not secret).
- Use RSA-OAEP padding instead of PKCS#1 v1.5 for asymmetric encryption.
