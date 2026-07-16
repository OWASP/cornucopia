## Scenario: Simon can bypass hashing and encryption functions because they are custom-written and/or inadequately implemented

Consider a scenario where Simon decompiles the app and finds a `customEncrypt(data, key)` method that XORs each byte of the data with the corresponding byte of the key, cycling through the key. He recognises this as a stream cipher with a short, repeating key. By XORing two intercepted ciphertexts produced with the same key position, the key cancels out and he can recover the XOR of the two plaintexts. With some known plaintext, he recovers the full key. The custom encryption was novel. It was also broken.

1. Custom cryptographic implementations almost always have weaknesses not present in vetted standard algorithms.
2. "Rolling your own crypto" replicates implementation errors that the cryptographic community has spent decades identifying and addressing.
3. Inadequately implemented standard algorithms (e.g., incorrect padding, missing IV, truncated MAC) can be as weak as custom algorithms.

### Example

Simon finds the app hashes passwords using a custom function: `hash = password.length + sum(bytes)`. Two different passwords can produce the same hash trivially. Simon finds a user whose hash is 1042 and submits "a" × 1042 as the password. The authentication accepts it. The custom hash function has catastrophic collision resistance. The developer had not studied cryptography; the developer had studied addition.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Spoofing**.

Custom or inadequately implemented cryptographic functions are almost always weaker than standard implementations, enabling an attacker to bypass the cryptographic protection or forge cryptographic values.

### What can go wrong?

- Custom hash functions with trivial collisions allow authentication bypass.
- Custom stream ciphers with repeating keys are recoverable from ciphertext-only.
- Incorrect padding implementation leaks information through timing or error responses.
- MAC truncation below 128 bits reduces resistance to birthday attacks.

### What are we going to do about it?

- Use industry-standard cryptographic libraries (Android Keystore / CryptoKit / BouncyCastle / libsodium) without modification.
- Never implement cryptographic primitives from scratch; the risk of subtle, exploitable errors is very high.
- If a standard algorithm is used, use it with the default, recommended parameters; do not modify the algorithm or its parameters.
- Have all cryptographic design and implementation reviewed by a cryptographer before deployment.
