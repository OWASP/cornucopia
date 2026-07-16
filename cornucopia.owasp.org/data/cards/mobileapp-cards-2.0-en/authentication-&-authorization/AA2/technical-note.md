## Technical Note: Jie can use the app to do sensitive operations because the “unlocked key” is not used during the application flow

### Platform Guidance

**Android:** Bind secret use to a key that requires user authentication and call it during the sensitive workflow itself, not just once during a cheerful login screen.

```kotlin
val spec = KeyGenParameterSpec.Builder(
"session-key",
KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_DECRYPT
).setUserAuthenticationRequired(true)
 .setUserAuthenticationParameters(30, KeyProperties.AUTH_BIOMETRIC_STRONG)
 .build()
```

**iOS:** Create Keychain items with `biometryCurrentSet` or `userPresence` access control so the secret cannot be reused silently after context changes.

```swift
let access = SecAccessControlCreateWithFlags(nil,
kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
[.biometryCurrentSet], nil)!
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0017, MASTG-TEST-0064
**New Tests:** MASTG-TEST-0326

### MASWE Weaknesses

- MASWE-0005, MASWE-0039: authentication-bound key usage and failures to reuse the protected key inside sensitive operations.
