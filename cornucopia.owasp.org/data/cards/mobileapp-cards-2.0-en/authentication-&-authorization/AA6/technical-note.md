## Platform-Aware Review Guidance

**Android**
- Use a `KeyStore` key with `setUserAuthenticationValidityDurationSeconds(-1)` for sensitive operations: this requires a fresh biometric prompt each time the key is used.
- Implement an application-level inactivity timer; on expiry, clear the in-memory session state and navigate to the authentication screen.
- For server-side operations, generate a server challenge, sign it with a user-authenticated key, and verify the signature server-side for each high-risk operation.

**iOS**
- `LAContext.invalidate()` before a high-risk operation: forces a new biometric evaluation even if a previous context is still valid.
- Use `kSecAccessControlBiometryCurrentSet` for keys that protect high-risk operations.
- Implement application-level session timeouts using `UIApplicationDelegate.applicationDidEnterBackground` to reset trust state after background transitions exceeding a threshold.

**Testing**
- Authenticate, wait for the inactivity timeout, then attempt a high-risk operation without re-authenticating; verify the app prompts for re-authentication.
- Authenticate, move the app to background for 5 minutes, bring it to foreground, and attempt a transfer; verify a re-auth prompt appears.
- Test with Frida: bypass the step-up prompt callback and verify the server-side challenge fails.

**OWASP Mappings**
- MASVS: AUTH-2, AUTH-3, PLATFORM-3
- MASTG: TEST-0018, TEST-0064, TEST-0268, TEST-0269, TEST-0326
- MASWE: MASWE-0028, MASWE-0029, MASWE-0045
