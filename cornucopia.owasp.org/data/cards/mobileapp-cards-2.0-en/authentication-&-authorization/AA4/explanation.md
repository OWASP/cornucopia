## Scenario: Vandana can bypass biometric authentication because the authentication is misconfigured or not implemented correctly

Consider a scenario where Vandana is a security researcher testing a mobile banking app. She notices the biometric authentication uses `BiometricPrompt` but does not bind the authentication result to a cryptographic operation via a `CryptoObject`. Instead, the app simply reads a boolean `authSucceeded` flag from the callback and proceeds. Vandana hooks the callback with a dynamic instrumentation tool, forces the boolean to `true`, and authenticates as the account owner without presenting a finger or face.

1. Biometric authentication that does not use a hardware-bound cryptographic operation can be bypassed by patching the result.
2. Fallback authentication (PIN, pattern) weaker than the app's security requirement may allow biometric bypass via the fallback path.
3. Incorrect biometric implementation may enrol the attacker's biometrics instead of requiring the user's existing biometrics.

### Example

Vandana attaches Frida to the running app process. She hooks `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded()` and injects a call with a fabricated `AuthenticationResult`. The app checks a boolean flag that the callback sets, finds it `true`, and opens the account. Vandana never presented a finger. The real account holder's biometrics were irrelevant, because they were never cryptographically verified — only confirmed by a flag in memory that anyone with instrumentation access could flip.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Vandana impersonates the legitimate user by manipulating the authentication outcome in memory or through a logic bypass, without defeating the biometric hardware itself.

### What can go wrong?

- Boolean-flag-based biometric gating is trivially bypassable with instrumentation tools on rooted/jailbroken devices.
- Fallback PIN authentication, if weaker, becomes the effective security boundary.
- Biometric changes (new fingerprint enrolled) are not detected, allowing a new person with device access to authenticate.

### What are we going to do about it?

- Always bind biometric authentication to a cryptographic operation: use `BiometricPrompt.CryptoObject` on Android, wrapping a `Cipher` initialised with a hardware-backed key configured with `setUserAuthenticationRequired(true)`.
- On iOS, use keys stored in the Secure Enclave with `kSecAccessControlBiometryCurrentSet` so that authentication is verified by hardware, not software.
- Set `setInvalidatedByBiometricEnrollment(true)` so that enrolling a new biometric invalidates the key, requiring re-enrolment.
- Do not rely solely on the boolean result of `onAuthenticationSucceeded`; rely on the ability to use the cryptographic key to decrypt or sign a challenge.
