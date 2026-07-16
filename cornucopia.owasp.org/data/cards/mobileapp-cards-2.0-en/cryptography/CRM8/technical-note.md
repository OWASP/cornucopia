## Platform-Aware Review Guidance

**Android**
- AES key size: `KeyGenParameterSpec.Builder(alias, PURPOSE).setKeySize(256)` for AES-256.
- RSA key size: `KeyPairGenerator.initialize(KeyGenParameterSpec.Builder(alias, PURPOSE).setKeySize(3072))`.
- Session tokens: `SecureRandom().generateSeed(16)` provides 128-bit entropy; Base64-encode for use as a token string.
- PBKDF2: `PBEKeySpec(password, salt, 600000, 256)` with `SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")`.

**iOS**
- `CryptoKit.SymmetricKey(size: .bits256)` for AES-256.
- `SecKeyCreateRandomKey` with `kSecAttrKeySizeInBits: 4096` for RSA; or use ECC P-256/P-384.
- `SecRandomCopyBytes(kSecRandomDefault, 16, bytes)` for 128-bit session tokens.
- Argon2id: use a vetted Swift/C library; CryptoKit does not include Argon2 natively.

**Testing**
- Review all key sizes against NIST SP 800-57 recommendations.
- Check PBKDF2 iteration counts against current hardware benchmarks.
- Review session token lengths for sufficient entropy against the expected number of concurrent active sessions.

**OWASP Mappings**
- MASVS: CRYPTO-1, CRYPTO-2
- MASTG: TEST-0013, TEST-0016, TEST-0061, TEST-0063, TEST-0204, TEST-0205, TEST-0208, TEST-0209, TEST-0309, TEST-0310, TEST-0311, TEST-0349
- MASWE: MASWE-0009, MASWE-0010, MASWE-0022, MASWE-0027
