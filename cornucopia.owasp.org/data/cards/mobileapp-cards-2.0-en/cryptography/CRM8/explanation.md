## Scenario: Adel can predict and use the app's cryptographic keys because they are insufficiently long and random, can be enumerated, or are derived from known values

Consider a scenario where Adel discovers the app generates 64-bit session keys using a CSPRNG. At first, this sounds acceptable — until Adel notes that the app is used by millions of users simultaneously. With 2^64 possible keys, a birthday attack at 2^32 operations has a 50% chance of finding a collision. With modern hardware generating millions of session tokens per second across a botnet, a collision-based attack becomes practical. The key length was secure for the 1990s.

1. 56-bit DES keys, 64-bit tokens, and 128-bit RSA keys do not meet current security standards.
2. Keys derived from user IDs, device serial numbers, or other enumerable values are not truly random.
3. PBKDF2 with a low iteration count (< 100,000 for 2024 hardware) reduces the cost of brute-force key derivation.

### Example

Adel finds the app's session tokens are 8 characters of alphanumeric (62^8 ≈ 2^47.6 possibilities). He runs a distributed enumeration attack across 10,000 devices, each generating 1 million token candidates per second. In about 2 days, he has found a valid active session token. The token entropy was too low for the threat model. A 128-bit token (22 alphanumeric characters) would have made this attack infeasible.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Spoofing**.

Insufficiently long or predictable keys can be enumerated or brute-forced, allowing an attacker to discover the key and either decrypt protected data or forge authenticated messages.

### What can go wrong?

- Short session tokens are brute-forced to find valid active sessions.
- Keys derived from enumerable inputs are predictable.
- Low PBKDF2 iteration counts allow offline brute-force of user passwords.
- 1024-bit RSA and 256-bit ECC keys provide insufficient security margins against modern cryptanalysis.

### What are we going to do about it?

- Use at least 128-bit keys for symmetric encryption (AES-128 minimum; AES-256 preferred for sensitive data).
- Use at least 2048-bit RSA keys (3072-bit or 4096-bit preferred); use at least 256-bit ECC keys.
- Generate session tokens with at least 128 bits of entropy from a CSPRNG.
- Configure PBKDF2 with at least 600,000 iterations for SHA-256 (NIST 2023 recommendation); use Argon2id for new implementations.
