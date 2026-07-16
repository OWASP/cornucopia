## Technical Note: Ade can bypass authentication because it is not enforced using a remote endpoint, or it is not based on a cryptographic primitive protected by keystore/keychain access control flags

### Platform Guidance

**Android:** For high-value actions, use a remote challenge signed with a Keystore-backed key that is protected by user authentication.

```kotlin
val keyGen = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_EC, "AndroidKeyStore")
keyGen.initialize(KeyGenParameterSpec.Builder("auth-key", KeyProperties.PURPOSE_SIGN)
.setUserAuthenticationRequired(true)
.build())
```

**iOS:** Use a Keychain/ Secure Enclave-backed key with access-control flags and have the server validate the signature instead of trusting a local boolean.

```swift
let access = SecAccessControlCreateWithFlags(nil,
kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
[.privateKeyUsage, .biometryCurrentSet], nil)!
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0017, MASTG-TEST-0018, MASTG-TEST-0064
**New Tests:** MASTG-TEST-0270

### MASWE Weaknesses

- MASWE-0036: cryptographic enforcement of authentication and missing remote verification.
