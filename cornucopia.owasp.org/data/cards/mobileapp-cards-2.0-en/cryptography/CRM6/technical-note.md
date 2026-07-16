## Technical Note: Kouti can extract sensitive data because the cryptographic key, used, is hard-coded or stored insecurely such as in local, internal/external storage

### Platform Guidance

**Android:** Store keys in Android Keystore, not in source code, assets, preferences, or bespoke “totally encrypted” JSON files.

```kotlin
val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
val secretKey = keyStore.getKey("app-key", null) as SecretKey
```

**iOS:** Keep secrets in Keychain or Secure Enclave with an appropriate accessibility class and never hard-code them into the bundle.

```swift
let query: [String: Any] = [
kSecClass as String: kSecClassGenericPassword,
kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
]
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0001, MASTG-TEST-0013, MASTG-TEST-0052, MASTG-TEST-0062
**New Tests:** MASTG-TEST-0221, MASTG-TEST-0311

### MASWE Weaknesses

- MASWE-0013, MASWE-0026: hard-coded or insecurely stored cryptographic keys.
