## Scenario: Ash can break the cryptography because it is not strong enough according to what is recommended or the perceived effort of a potential attacker

Consider a scenario where Ash discovers the app uses DES (56-bit key, effectively ~57 bits of security) for data encryption. Modern hardware can brute-force DES in under 24 hours. The algorithm was retired by NIST in 2005. The developer had chosen it because it was available in the legacy Java `Cipher` API and "it was already there." Ash breaks the encryption and reads all stored user data.

1. DES, 3DES (TDEA), RC4, MD5, and SHA-1 are deprecated algorithms that no longer meet current security requirements.
2. Using short key lengths (1024-bit RSA, 512-bit ECC, 128-bit AES for post-quantum scenarios) provides insufficient security margin.
3. Relying on "it was the default" without checking current recommendations leads to the use of deprecated algorithms.

### Example

Ash finds the app uses `Cipher.getInstance("DES/ECB/PKCS5Padding")`. He captures 200 bytes of ciphertext from a network response. He uses a DES brute-force tool (cloud-based, approximately $50 for the required computation) and recovers the plaintext within 18 hours. The developer's choice of DES was motivated by copy-pasting a Stack Overflow answer from 2006. The answer was wrong then too.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Weak cryptographic algorithms can be broken with resources available to motivated attackers, rendering the cryptographic protection ineffective.

### What can go wrong?

- Data encrypted with DES/3DES is recoverable with modest computational resources.
- MD5-hashed passwords are reversible using precomputed rainbow tables.
- RC4-encrypted traffic is recoverable using known statistical attacks.
- SHA-1 collisions enable certificate or document forgery.

### What are we going to do about it?

- Use AES-256-GCM or ChaCha20-Poly1305 for symmetric encryption.
- Use SHA-256, SHA-384, or SHA-512 for hashing; SHA-3 for new implementations.
- Use RSA with 3072-bit keys (or 4096-bit); prefer ECDSA P-256 or P-384 for signatures.
- Use Argon2id for password hashing; bcrypt or scrypt as alternatives.
- Review all cryptographic algorithm choices against current NIST SP 800-131A recommendations.
