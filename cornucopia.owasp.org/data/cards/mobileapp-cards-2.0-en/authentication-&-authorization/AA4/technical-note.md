## Technical Note: Vandana can bypass biometric authentication because the authentication is misconfigured or not implemented correctly

### Platform Guidance

**Android:** Use `BiometricPrompt` with strong authenticators only when the action really requires biometrics and do not silently downgrade to weaker factors.

```kotlin
val promptInfo = BiometricPrompt.PromptInfo.Builder()
.setTitle("Approve transfer")
.setAllowedAuthenticators(BIOMETRIC_STRONG)
.build()
```

**iOS:** Prefer `LAPolicy.deviceOwnerAuthenticationWithBiometrics` for biometric-only flows and handle lockout or unavailable states explicitly.

```swift
let context = LAContext()
if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: nil) {
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Approve transfer") { _, _ in }
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0018, MASTG-TEST-0064
**New Tests:** MASTG-TEST-0328

### MASWE Weaknesses

- MASWE-0029, MASWE-0041: biometric policy selection, authenticator strength, and unsafe fallback behavior.
