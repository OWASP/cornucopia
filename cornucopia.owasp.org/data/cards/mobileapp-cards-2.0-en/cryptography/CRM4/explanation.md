## Scenario: Enselme can modify sensitive data (stored or in transit) because it is not subject to integrity checking

Consider a scenario where Enselme has root access to a device. The banking app stores the user's account tier (`"premium"`, `"standard"`) in an encrypted database. The encryption uses AES-CBC without any authentication tag. Enselme modifies a specific byte in the ciphertext using a bit-flipping attack on the CBC-mode ciphertext, changing the decrypted value from `"standard"` to `"premium"`. The app reads the decrypted (but modified) value without detecting the tampering, and grants Enselme premium features. The encryption provided confidentiality; it did not provide integrity.

1. CBC mode encryption without a MAC provides confidentiality but not integrity.
2. ECB mode additionally leaks data patterns and is trivially block-swappable.
3. Data signed only with a checksum (CRC32, MD5) can be forged by an attacker who can compute the same function.

### Example

Enselme intercepts a network response encrypted with AES-CBC. The response contains a `"admin": false` field. Using knowledge of the CBC structure and the predictable plaintext format, he flips the bit corresponding to `false` to `true` in the ciphertext. The app decrypts the modified ciphertext and processes `"admin": true`. The modification was undetected because no MAC was computed over the ciphertext. AES-CBC encrypted the data. It did not protect it from modification.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering**.

Encryption without authentication allows an attacker who can modify the ciphertext to alter the plaintext in predictable ways (CBC bit-flipping) or substitute entire ciphertext blocks (ECB block substitution), tampering with the data without detection.

### What can go wrong?

- CBC bit-flipping attacks modify specific bytes of the decrypted plaintext.
- ECB block substitution reorders or replaces blocks of the decrypted data.
- Unauthenticated ciphertext in network responses is modified by an on-path attacker to alter application state.

### What are we going to do about it?

- Use authenticated encryption: AES-GCM or ChaCha20-Poly1305. These modes provide both confidentiality and integrity in a single primitive.
- If using AES-CBC for legacy compatibility, always apply Encrypt-then-MAC: compute HMAC-SHA256 over the ciphertext and IV, verify the MAC before decrypting.
- Never use ECB mode for any data that is more than one block in size.
