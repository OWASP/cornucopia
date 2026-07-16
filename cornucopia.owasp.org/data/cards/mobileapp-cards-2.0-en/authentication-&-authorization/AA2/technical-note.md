## Platform-Aware Review Guidance

**Android**
- Create cryptographic keys with `KeyGenParameterSpec.Builder`:
  - `setUserAuthenticationRequired(true)` — key is not usable without a user-authentication event.
  - `setUserAuthenticationValidityDurationSeconds(-1)` — requires biometric prompt per-use (most secure for sensitive operations); a positive value allows a time window.
  - `setInvalidatedByBiometricEnrollment(true)` — key is invalidated if new biometrics are enrolled.
- Use `BiometricPrompt` with `CryptoObject` wrapping a `Cipher` to ensure the authentication is cryptographically bound to the key operation.
- Check that the app calls `cipher.init(DECRYPT_MODE, key)` after `BiometricPrompt.authenticate()` resolves, not before.

**iOS**
- Use `SecAccessControl` with `kSecAccessControlBiometryCurrentSet` or `kSecAccessControlUserPresence` when storing keys in the Secure Enclave.
- `LAContext.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, ...)` without a `SecAccessControl`-bound key is bypassable on jailbroken devices — always bind the key.
- For step-up auth, call `LAContext.invalidate()` to clear the cached authentication context before a sensitive operation.

**Testing**
- Use objection / Frida to hook `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded` and return `true` without actual authentication; verify the app rejects the operation.
- Lock the screen mid-session, resume the app, and confirm that sensitive data is not accessible before re-authentication.

**OWASP Mappings**
- MASVS: AUTH-2, AUTH-3, CRYPTO-2
- MASTG: TEST-0017, TEST-0018, TEST-0064, TEST-0270, TEST-0271, TEST-0328
- MASWE: MASWE-0018, MASWE-0031, MASWE-0043, MASWE-0046
