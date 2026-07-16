## Scenario: Orace can predict the seed value used for generating cryptographic keys, thereby compromising the cryptographic key

Consider a scenario where Orace discovers the app seeds the random number generator with `System.currentTimeMillis()`. The app generates a session key at login time. Orace knows the approximate login time (±5 minutes) from the server access log timestamp in an error response. He enumerates all millisecond timestamps in that 10-minute window — about 600,000 values — and for each, re-seeds the RNG and generates the key. One of those keys decrypts the captured session. The predictable seed made the key exhaustively searchable.

1. Seeding a PRNG with predictable values (time, device ID, user ID) makes the PRNG output predictable.
2. Using a non-CSPRNG (Pseudo-Random Number Generator) for cryptographic key generation produces keys that can be predicted by an attacker who knows the seed.
3. Using `Random` (Java) or `rand()` (C) instead of `SecureRandom` / `CSPRNG` produces weak cryptographic material.

### Example

Orace finds the app uses `new Random(System.nanoTime())` for generating an AES key. `System.nanoTime()` has limited entropy on many devices and is observable through timing side channels. He narrows down the nanoTime value to a range of a few thousand values using observable timing, enumerates the range, and recovers the key. The AES-256 key had only the entropy of the seed — far less than 256 bits.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

A predictable seed produces a predictable key. An attacker who can predict or enumerate the seed can recover the key and decrypt all data protected by it.

### What can go wrong?

- Session keys, encryption keys, and cryptographic tokens are recoverable by an attacker who predicts the RNG seed.
- Token enumeration: if tokens are generated from a predictable PRNG, they can be enumerated to find valid tokens.
- All data encrypted with the predictable key is retroactively compromised once the seed is recovered.

### What are we going to do about it?

- Use `SecureRandom` (Android) or `SecRandomCopyBytes` / `CryptoKit` random functions (iOS) for all cryptographic key generation.
- Never seed `SecureRandom` with a predictable value; the default constructor uses OS entropy.
- Never use `java.util.Random`, `Math.random()`, `rand()`, or `srand(time(NULL))` for cryptographic purposes.
