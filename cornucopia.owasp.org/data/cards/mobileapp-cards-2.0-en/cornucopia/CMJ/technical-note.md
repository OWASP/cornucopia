## Platform-Aware Review Guidance

**Android**
- AES-GCM: `Cipher.getInstance("AES/GCM/NoPadding")` — `doFinal()` throws `AEADBadTagException` if the tag is invalid; this must not be caught silently.
- For end-to-end encrypted sync: sign the encrypted payload with ECDSA using a per-user key; verify the signature server-side and client-side before applying the sync.

**iOS**
- `CryptoKit.AES.GCM.open(_:using:)` throws `CryptoKitError.authenticationFailure` on tag verification failure; propagate this error.
- For end-to-end encrypted data: use `CryptoKit.P256.Signing.PrivateKey` for ECDSA signing; verify on receipt before decryption.

**Cloud Sync Architecture**
- Never apply synced data without verifying its integrity and authenticity.
- Implement version vectors or sequence numbers in the sync protocol to detect replay and ordering attacks.
- Consider content-addressed storage (hash of the plaintext) for integrity verification without key sharing.

**Testing**
- Intercept the sync payload and modify a byte; verify the receiving client detects and rejects the modified payload.
- Test with a valid ciphertext but a stripped authentication tag; verify rejection.

**OWASP Mappings**
- MASVS: CODE-4, CRYPTO-1
- MASTG: TEST-0002
- MASWE: MASWE-0024, MASWE-0026
