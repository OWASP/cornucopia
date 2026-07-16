## Technical Note: Titus can patch out critical functionality because the runtime integrity checks are not strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Check code and environment integrity at runtime for the parts of the app that gate high-risk actions, and send the verdict to the backend before honoring them.

```kotlin
val verdict = playIntegrityClient.requestIntegrityToken(request)
api.submitIntegrity(verdict)
```

**iOS:** Use attestation, signed configuration, and runtime checks together so patched clients cannot quietly skip critical protections.

```swift
let isTampered = !bundleVerifier.signatureMatchesExpectedHash()
if isTampered { throw IntegrityError.modified }
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0050
**New Tests:** MASTG-TEST-0324, MASTG-TEST-0248

### MASWE Weaknesses

- MASWE-0097: runtime integrity weaknesses that allow patching out critical functionality.
