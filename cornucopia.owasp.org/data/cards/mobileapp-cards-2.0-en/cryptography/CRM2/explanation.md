## Scenario: Lesego can compromise cryptographic operations and resources because keys are reused for multiple purposes or not used according to the purpose for which they were created

Consider a scenario where Lesego discovers the target app uses a single master key for both encryption of stored data and for signing API requests. She extracts the key from a rooted device (it was not hardware-protected). She now has a key that signs valid API requests — because the developer reused the same key for both operations. Key reuse means key compromise has a multiplied blast radius.

1. Using the same key for encryption and signing violates the principle of cryptographic key separation.
2. Using a key beyond its intended purpose (e.g., using an authentication key for data encryption) creates unexpected security dependencies.
3. Key reuse across different app versions or users creates cross-context vulnerabilities.

### Example

Lesego observes that the app uses the same RSA key pair for TLS certificate authentication AND for signing financial transactions. She extracts the private key from a compromised device. She can now sign arbitrary transactions as if they originated from the legitimate user's device. The developer had reasoned that "it's the same key, so it's the same security." The security was the same — compromised in both contexts simultaneously.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Tampering**.

Key reuse means that compromise of a key used for one purpose immediately compromises all other operations that depend on the same key.

### What can go wrong?

- A key extracted for one purpose (e.g., analytics signing) can be used for another (e.g., transaction signing).
- Key rotation in one context does not protect the other contexts that shared the key.
- Cryptographic guarantees (separation of concern between confidentiality and authenticity) are violated.

### What are we going to do about it?

- Generate separate keys for each cryptographic purpose: separate keys for encryption, signing, authentication, and key derivation.
- Use key usage extensions (X.509 KeyUsage, Android KeyStore `setKeyUsages`) to restrict each key to its designated purpose.
- Implement key derivation from a master secret using HKDF with distinct info strings for each purpose (e.g., `HKDF(master, "data-encryption")`, `HKDF(master, "api-signing")`).
- Document the purpose of each cryptographic key in the key management registry.
