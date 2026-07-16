## Technical Note: Kim can reduce app users' privacy because the app repurpose biometric information (e.g. fingerprints, facial recognition data, etc.) collected for security concerns in order to cater for commercial interests

### Platform Guidance

**Android:** Biometric templates and signals used for local auth should not be copied into analytics, personalization, or training pipelines. That is not “synergy,” that is a regulatory speedrun.

```kotlin
require(!event.containsBiometricSignals)
biometricResult = null // use only as auth result, not as retained data
```

**iOS:** Treat biometric outputs as strictly scoped authentication signals and do not repurpose them for product or business features.

```swift
guard useCase == .authenticateUser else { throw PrivacyError.invalidUse }
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** MASTG-TEST-0257, MASTG-TEST-0361

### MASWE Weaknesses

- MASWE-0112: misuse and repurposing of biometric information beyond the security purpose it was collected for.
