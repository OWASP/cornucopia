## Platform-Aware Review Guidance

**Android**
- Use `javax.crypto` / `java.security` providers backed by `AndroidKeyStore` or `BouncyCastle`.
- Use `MessageDigest.getInstance("SHA-256")` — not a custom hash.
- Use `Mac.getInstance("HmacSHA256")` — not a custom HMAC.
- Static analysis: grep for `XOR`, `ROL`, `ROT`, custom loop-based `encrypt`/`hash` methods, bit-manipulation on byte arrays adjacent to crypto operations.

**iOS**
- Use `CryptoKit` (iOS 13+) for all new cryptographic operations: AES.GCM, ChaChaPoly, HMAC, SHA256/384/512, P256/P384/P521.
- CommonCrypto is acceptable for AES, HMAC, SHA-256; do not use it to implement custom modes.
- libsodium is a vetted, high-level cryptographic library for scenarios not covered by CryptoKit.

**Design Review**
- Any novel cryptographic construction (combining standard primitives in a custom way) requires external cryptographic review before production use.
- "Encrypt-then-MAC" and "AEAD" are the only safe authenticated encryption constructions; all others require expert review.

**OWASP Mappings**
- MASVS: CODE-3, CRYPTO-1
- MASTG: TEST-0014, TEST-0061, TEST-0211
- MASWE: MASWE-0019, MASWE-0021
