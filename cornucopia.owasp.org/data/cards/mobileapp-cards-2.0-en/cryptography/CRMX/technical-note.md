## Platform-Aware Review Guidance

**Deprecated Algorithms (never use)**
- Symmetric: DES, 3DES/TDEA, RC4, RC2, Blowfish (for new implementations), AES-ECB
- Hash (for security): MD5, SHA-1 (acceptable only for non-security checksums with awareness)
- Asymmetric: RSA < 2048-bit, DSA < 2048-bit, ECC < 224-bit

**Approved Algorithms (current)**
- Symmetric encryption: AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305
- Hash: SHA-256, SHA-384, SHA-512, SHA-3 (256/384/512)
- Password hashing: Argon2id (preferred), bcrypt, scrypt
- Asymmetric: RSA-3072+, ECDSA P-256/P-384, Ed25519

**Android**
- `Cipher.getInstance("AES/GCM/NoPadding")` — correct.
- `MessageDigest.getInstance("SHA-256")` — correct for non-password hashing.
- Static analysis: grep for `DES`, `RC4`, `MD5`, `SHA1` in `Cipher.getInstance`, `MessageDigest.getInstance`, `Mac.getInstance`.

**iOS**
- `CryptoKit.AES.GCM`, `CryptoKit.ChaChaPoly` — AEAD ciphers.
- `CryptoKit.SHA256`, `SHA384`, `SHA512` — approved hash functions.
- CommonCrypto: avoid `kCCAlgorithmDES`, `kCCAlgorithm3DES`; use `kCCAlgorithmAES`.

**OWASP Mappings**
- MASVS: CODE-3, CRYPTO-1
- MASTG: TEST-0013, TEST-0014, TEST-0061, TEST-0210, TEST-0211, TEST-0221, TEST-0232, TEST-0312, TEST-0317, TEST-0350
- MASWE: MASWE-0019, MASWE-0020, MASWE-0021, MASWE-0023
