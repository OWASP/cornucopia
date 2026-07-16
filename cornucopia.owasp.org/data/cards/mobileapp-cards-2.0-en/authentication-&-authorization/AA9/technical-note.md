## Platform-Aware Review Guidance

**Android**
- `BiometricPrompt.AuthenticationCallback` has three callbacks: `onAuthenticationSucceeded`, `onAuthenticationError`, `onAuthenticationFailed`.
- Only `onAuthenticationSucceeded` should transition authentication state to "authenticated".
- In `onAuthenticationError` and `onAuthenticationFailed`, explicitly set state to "not authenticated" and show the login screen.
- Use crypto-based authentication: if `cipher.doFinal()` succeeds, the user is authenticated — if it throws, they are not. No boolean flag needed.

**iOS**
- `LAContext.evaluatePolicy` completion handler: only proceed on `success == true && error == nil`.
- If `error` is `LAError.biometryNotAvailable`, `biometryNotEnrolled`, or `biometryLockout`, navigate to an alternative authentication method — not to an authenticated state.
- For Secure Enclave key operations: `SecKeyCreateSignature` / `SecKeyDecrypt` failing means the key was not unlocked; treat failure as unauthenticated.

**Testing**
- Trigger biometric API errors (cover sensor, exhaust retry limit, revoke permissions) during authentication and verify the app reaches the login screen, not the authenticated state.
- Use Frida to throw exceptions from the biometric callback and observe the app's response.
- Disconnect from the network during remote authentication; verify the app denies access rather than allowing offline mode.

**OWASP Mappings**
- MASVS: AUTH-2
- MASTG: TEST-0017, TEST-0018, TEST-0064
- MASWE: (see MASVS references above)
