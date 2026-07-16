## Platform-Aware Review Guidance

**Android**
- For configuration integrity: sign the configuration JSON server-side with ECDSA and verify the signature in the app using the hardcoded public key.
- `KeyStore`-backed HMAC: generate an HMAC key in the Android Keystore (not extractable); use it to compute and verify HMACs over local files.
- SQLite database integrity: SQLCipher with a Keystore-derived key provides both encryption and implicit integrity (HMAC over each page).

**iOS**
- For configuration files: sign server-side with ECDSA; verify in app using `SecKeyVerifySignature` with the hardcoded public key.
- Keychain-stored HMAC keys: use `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` to bind to the device; cannot be exported.
- `CommonCrypto.CCHmac` with a Keychain-protected key for local file HMAC.

**Testing**
- Modify a local configuration file; verify the app detects the tampering and refuses to apply the modified configuration.
- On a rooted device, replace the file and compute a new HMAC/checksum; verify the app's verification rejects the modification (because the key is hardware-protected and cannot be used to forge the HMAC).

**OWASP Mappings**
- MASVS: CODE-4, RESILIENCE-2
- MASTG: TEST-0002, TEST-0047, TEST-0090, TEST-0338, TEST-0387
- MASWE: MASWE-0105
