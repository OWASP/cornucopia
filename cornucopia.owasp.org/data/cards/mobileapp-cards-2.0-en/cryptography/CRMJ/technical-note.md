## Technical Note: Hassan can extract or modify sensitive data because functions for storage and/or encryption are weak, deprecated or used incorrectly

### Platform Guidance

**Android:** Deprecate weak storage and crypto helpers proactively and replace legacy APIs with current platform primitives before the auditors arrive with clipboards.

```kotlin
// Prefer EncryptedSharedPreferences replacement backed by Keystore-managed keys
val spec = MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
```

**iOS:** Review for deprecated CommonCrypto patterns, ECB-like constructions, and storage helpers that skip modern integrity protection.

```swift
// Prefer CryptoKit AES.GCM or ChaChaPoly over home-grown wrappers
let sealed = try AES.GCM.seal(data, using: key)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0001, MASTG-TEST-0014, MASTG-TEST-0052, MASTG-TEST-0061
**New Tests:** MASTG-TEST-0310

### MASWE Weaknesses

- MASWE-0018: weak, deprecated, or incorrectly combined storage and cryptographic functions.
