## Platform-Aware Review Guidance

**Android**
- Preferred: `Cipher.getInstance("AES/GCM/NoPadding")` — AEAD mode, provides both encryption and integrity.
- GCM parameters: use a 96-bit (12-byte) random nonce; never reuse a nonce with the same key.
- If CBC is required for interoperability: `Mac.getInstance("HmacSHA256")` — compute over `IV || ciphertext` and verify before decryption.
- Lint/static analysis: flag `AES/CBC/PKCS5Padding` usage in code review.

**iOS**
- `CryptoKit.AES.GCM.seal(_:using:nonce:)` — authenticated encryption, returns `SealedBox` containing ciphertext + tag.
- `CryptoKit.ChaChaPoly.seal(_:using:nonce:)` — alternative AEAD cipher, often preferred for software implementations.
- CommonCrypto does not natively provide GCM; use CryptoKit (iOS 13+) or a vetted third-party library for GCM.

**Testing**
- Attempt to modify the ciphertext stored by the app; verify the app detects the modification (GCM authentication tag failure) and rejects the data.
- Review all `Cipher.getInstance()` calls for CBC mode usage; flag for authentication review.

**OWASP Mappings**
- MASVS: CODE-4, CRYPTO-1
- MASTG: TEST-0002
- MASWE: MASWE-0024, MASWE-0025, MASWE-0026
