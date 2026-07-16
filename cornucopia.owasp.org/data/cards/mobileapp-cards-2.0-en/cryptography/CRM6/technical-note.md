## Platform-Aware Review Guidance

**Android**
- Generate keys in the `KeyStore`: `KeyGenerator.getInstance("AES", "AndroidKeyStore")`.
- Keys generated in the `AndroidKeyStore` cannot be exported; they are hardware-protected on devices with StrongBox or TEE.
- Static analysis: grep for `SecretKeySpec`, `new byte[] { ... }`, string constants adjacent to `Cipher.getInstance` calls.
- MobSF: "Hardcoded Secrets" finding.

**iOS**
- `CryptoKit.SymmetricKey(size:)` — generate a new key at first run and store it in the Keychain with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`.
- For Secure Enclave operations: generate an asymmetric key with `kSecAttrTokenIDSecureEnclave`; private key never leaves the Enclave.
- Static analysis: grep for hardcoded byte arrays or strings near `CCCrypt`, `SecKeyEncrypt`, or `AES.GCM.seal`.

**Testing**
- Decompile the APK/IPA and search for hardcoded key material: constant byte arrays, Base64-encoded strings of key length near cryptographic API calls.
- On a rooted/jailbroken device, extract `SharedPreferences` / `UserDefaults` and check for key material.

**OWASP Mappings**
- MASVS: AUTH-1, CRYPTO-1, CRYPTO-2, NETWORK-1, STORAGE-1
- MASTG: TEST-0001, TEST-0013, TEST-0052, TEST-0062, TEST-0212, TEST-0213, TEST-0214
- MASWE: MASWE-0005, MASWE-0014, MASWE-0017, MASWE-0036
