## Platform-Aware Review Guidance

**Android KeyStore**
- `KeyGenParameterSpec.Builder.setKeyUsages(KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)` — restricts key to encryption/decryption only; a separate key must be generated for signing.
- Generate distinct `KeyStore` aliases for each purpose: `"app-data-encryption-key"`, `"app-api-signing-key"`, `"app-auth-key"`.
- For key derivation from a master secret: use `SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")` or HKDF with domain-separated info strings.

**iOS Keychain / Secure Enclave**
- Generate separate `SecKey` instances for each purpose; set `kSecAttrKeyUsage` (RSA) or appropriate flags.
- Secure Enclave keys are always asymmetric; derive symmetric keys using ECDH key agreement + HKDF.
- Use separate Keychain items with descriptive `kSecAttrLabel` for audit and key lifecycle management.

**Key Derivation**
- HKDF (RFC 5869): `HKDF-Expand(PRK, info="purpose-label", length)` — use distinct `info` strings to derive purpose-separated keys from a single master.
- Never use the same derived key for both encryption and HMAC.

**Testing**
- Enumerate all `KeyStore` aliases; verify no alias is used for multiple purposes.
- Review all `Cipher.getInstance()`, `Mac.getInstance()`, and `Signature.getInstance()` calls; verify each uses the appropriate purpose-specific key alias.

**OWASP Mappings**
- MASVS: AUTH-2, AUTH-3, CRYPTO-2
- MASTG: TEST-0015, TEST-0062, TEST-0307, TEST-0308
- MASWE: MASWE-0011, MASWE-0012, MASWE-0018
