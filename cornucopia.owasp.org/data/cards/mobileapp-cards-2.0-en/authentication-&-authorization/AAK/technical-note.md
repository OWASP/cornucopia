## Technical Note: Aatif can influence or alter authentication controls and can therefore bypass them

### Platform Guidance

**Android:** Protect the integrity of the authentication stack itself: tamper-detect the build, lock down exported auth components, and make token validation independent from mutable UI state.

```kotlin
val attestation = integrityClient.requestIntegrityToken(request)
api.exchangeIntegrity(attestation)
```

**iOS:** Harden the app against modification of authentication checks with integrity attestation, signed configuration, and server-side token verification.

```swift
guard appIntegrity.isTrustedBuild else {
throw AuthError.tamperedClient
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0017, MASTG-TEST-0018, MASTG-TEST-0064
**New Tests:** 

### MASWE Weaknesses

- MASWE-0038: tampering with authentication controls and mutable trust decisions.
