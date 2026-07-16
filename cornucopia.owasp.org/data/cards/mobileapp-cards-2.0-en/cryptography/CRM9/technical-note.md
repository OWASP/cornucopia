## Platform-Aware Review Guidance

**Android**
- Do not catch `KeyStoreException`, `UnrecoverableKeyException`, or `InvalidKeyException` and continue without the key.
- Correct pattern:
  ```kotlin
  val decrypted = try {
      cipher.doFinal(ciphertext)
  } catch (e: AEADBadTagException) {
      throw SecurityException("Decryption failed: data integrity check failed", e)
  }
  // Only use decrypted if no exception was thrown
  ```
- Handle `KeyPermanentlyInvalidatedException` by prompting the user to re-enrol biometrics and re-encrypt data with a new key — not by returning plaintext.

**iOS**
- `SecKeyDecrypt` / `CryptoKit.AES.GCM.open` failure: propagate the error to the caller; do not return the original ciphertext or plaintext.
- `SecItem` not found (`errSecItemNotFound`): prompt for re-authentication or re-setup; do not fall back to unprotected storage.
- `AES.GCM.SealedBox.init` throws on authentication failure: always check for this error and handle it as data corruption/tampering, not a transparent fallback.

**Testing**
- Delete the app's `KeyStore` / Keychain key entry; verify the app refuses to return plaintext data.
- Induce a `KeyStoreException` by revoking the key; verify the app displays an error and requires re-authentication.
- Review all `try/catch` blocks around cryptographic operations for incorrect fallback behaviour.

**OWASP Mappings**
- MASVS: CRYPTO-1
- MASTG: TEST-0014
- MASWE: (see MASVS references above)
