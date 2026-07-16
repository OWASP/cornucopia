## Platform-Aware Review Guidance

**Android**
- `BiometricPrompt.authenticate(promptInfo, cryptoObject)` — the `CryptoObject` must wrap a `Cipher`, `Mac`, or `Signature` backed by a `KeyStore` key with `setUserAuthenticationRequired(true)`.
- Verify that the app attempts the cryptographic operation (decrypt/sign) after `onAuthenticationSucceeded`, and only proceeds if the operation succeeds.
- `setInvalidatedByBiometricEnrollment(true)` — key is invalidated when a new biometric is enrolled; the app must handle `KeyPermanentlyInvalidatedException` gracefully.
- Do not fall back to a weaker authentication method silently; display a clear message and re-prompt or require remote authentication.

**iOS**
- `SecAccessControl` with `kSecAccessControlBiometryCurrentSet` ties the key to currently enrolled biometrics; enrolling a new face/finger invalidates the key.
- `LAContext.setCredential(_:type:)` is not needed when using Secure Enclave-backed keys — the Enclave handles the verification.
- Do not use `LAContext.evaluatePolicy` alone for high-security operations; always require a successful cryptographic operation with a Secure Enclave key.

**Testing**
- Use Frida to hook `BiometricPrompt.AuthenticationCallback.onAuthenticationSucceeded` and call it without actual authentication; verify the app does not proceed.
- On a jailbroken iOS device, use objection to bypass biometric checks; verify the cryptographic operation still fails.
- Enrol a new biometric after key creation; verify the app detects invalidation and requires re-enrolment.

**OWASP Mappings**
- MASVS: AUTH-2, CRYPTO-2
- MASTG: TEST-0017, TEST-0018, TEST-0064, TEST-0266, TEST-0267, TEST-0268, TEST-0269, TEST-0270, TEST-0271, TEST-0326, TEST-0327, TEST-0328, TEST-0329, TEST-0330
- MASWE: MASWE-0044, MASWE-0045, MASWE-0046
