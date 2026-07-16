## Technical Note: Erlend can compromise the app by running it in an emulator because the prevention against emulators are not strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Detect emulator signals only to raise risk or block sensitive workflows; do not assume the environment is trustworthy just because it looks like a phone wearing a convincing hat.

```kotlin
val suspicious = Build.FINGERPRINT.contains("generic") ||
Build.MODEL.contains("sdk_gphone")
if (suspicious) requireStepUpReview()
```

**iOS:** Look for simulator-only artefacts and hook-friendly environments, but keep the final trust decision in backend or attestation logic.

```swift
#if targetEnvironment(simulator)
let runningInSimulator = true
#endif
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0049, MASTG-TEST-0092
**New Tests:** MASTG-TEST-0249, MASTG-TEST-0219, MASTG-TEST-0402

### MASWE Weaknesses

- MASWE-0092, MASWE-0106: emulator and non-genuine-environment detection weaknesses.
