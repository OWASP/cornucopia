## Platform-Aware Review Guidance

**Android**
- Cipher: `Cipher.getInstance("AES/GCM/NoPadding")` for authenticated encryption.
- Key management: `KeyStore`-backed `SecretKey` with `KeyGenParameterSpec.PURPOSE_ENCRYPT | PURPOSE_DECRYPT`.
- Static analysis: grep for `Base64.encode`, `XOR`, or custom `encode`/`scramble` methods applied to sensitive data.

**iOS**
- `CryptoKit.AES.GCM.seal(_:using:nonce:)` — authenticated encryption with a generated `SymmetricKey`.
- CommonCrypto: `CCCrypt(kCCEncrypt, kCCAlgorithmAES, kCCOptionPKCS7Padding, ...)` — use AES in an authenticated mode.
- Static analysis: grep for `Data.base64EncodedString()`, manual XOR loops, and custom "encryption" functions applied to sensitive data.

**Testing**
- Extract stored sensitive data and attempt base64/hex decoding; verify it does not yield plaintext.
- Decompile and search for encoding methods applied to sensitive values instead of cryptographic cipher calls.

**OWASP Mappings**
- MASVS: CRYPTO-1
- MASTG: TEST-0014, TEST-0061
- MASWE: (see MASVS references above)
