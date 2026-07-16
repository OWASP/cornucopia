## Platform-Aware Review Guidance

**Android**
- `KeyGenParameterSpec.Builder.setUserAuthenticationRequired(true)` — key cannot be used without a recent user-authentication event.
- `setIsStrongBoxBacked(true)` — key stored in hardware-isolated StrongBox (where available); not extractable even with root.
- Do not store authentication state in `SharedPreferences` or any world-readable location; derive state from the ability to perform a key operation.

**iOS**
- Use the Secure Enclave: `kSecAttrTokenIDSecureEnclave` in `SecKeyCreateRandomKey` attributes; the private key never leaves the Secure Enclave.
- `kSecAccessControlBiometryCurrentSet` — key requires current biometrics; new enrolment invalidates.
- Do not store `isLoggedIn` in `UserDefaults`; treat authentication as the ability to perform a Secure Enclave operation successfully.

**Remote Session Validation**
- Issue short-lived access tokens (JWT exp ≤ 15 minutes) with refresh tokens stored securely.
- Require the client to present a valid access token on every API call; do not implement "trust the local flag" mode.
- Provide a server-side token revocation endpoint for stolen-device scenarios.

**Testing**
- On a rooted device, modify `SharedPreferences`/`UserDefaults` authentication flags and verify the app does not proceed without a valid server token.
- Attempt to use the local cryptographic key from a different app process on a rooted device; verify access is denied.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-2, CODE-3, STORAGE-1
- MASTG: TEST-0017, TEST-0018, TEST-0064
- MASWE: MASWE-0005, MASWE-0032, MASWE-0033, MASWE-0035, MASWE-0041
