## Platform-Aware Review Guidance

**Android**
- CBC: generate IV with `SecureRandom().nextBytes(iv)`; store as `IV || ciphertext`; extract on decryption with `GCMParameterSpec(128, iv)`.
- GCM: `GCMParameterSpec(128, nonce)` — 96-bit nonce, fresh per-message, never reused.
- RSA: `Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")` — OAEP padding.
- Static analysis: grep for `IvParameterSpec(new byte[16])` (zero IV), `new byte[]{0,0,...}` used as IV.

**iOS**
- `CryptoKit.AES.GCM.seal(_:using:)` without specifying a nonce generates one automatically — this is the safe default.
- `AES.GCM.Nonce()` generates a random nonce; `AES.GCM.Nonce(data:)` with a fixed value is dangerous.
- CommonCrypto CBC: `CCCrypt` requires an IV parameter; never pass a fixed constant; generate with `SecRandomCopyBytes`.

**Testing**
- Encrypt the same plaintext twice with the same key; verify the ciphertexts are different (random IV/nonce).
- Inspect IV extraction from stored ciphertexts; verify IVs are unique across different encryption operations.
- Test with a Padding Oracle attack against PKCS#1 v1.5 RSA implementations.

**OWASP Mappings**
- MASVS: CODE-3, CRYPTO-1, CRYPTO-2, STORAGE-1
- MASTG: TEST-0001, TEST-0013, TEST-0014, TEST-0052, TEST-0061, TEST-0210, TEST-0211, TEST-0221, TEST-0232, TEST-0312, TEST-0317, TEST-0350
- MASWE: MASWE-0015, MASWE-0019, MASWE-0020, MASWE-0021, MASWE-0023
