## Technical Note: Lesego can compromise cryptographic operations and resources because keys are reused for multiple purposes, or not used according to the purpose for which they were created

### Platform Guidance

**Android:** Generate separate keys for encryption, signing, MAC, and wrapping; a Swiss-army key is convenient until it cuts the threat model.

```kotlin
val encSpec = KeyGenParameterSpec.Builder("enc-key", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT).build()
val signSpec = KeyGenParameterSpec.Builder("sign-key", KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY).build()
```

**iOS:** Create distinct Keychain or Secure Enclave keys per purpose and document their allowed operations.

```swift
let signingTag = "org.example.signing".data(using: .utf8)!
let encryptionTag = "org.example.encryption".data(using: .utf8)!
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0015, MASTG-TEST-0062
**New Tests:** MASTG-TEST-0204, MASTG-TEST-0210

### MASWE Weaknesses

- MASWE-0009, MASWE-0022: key separation and improper reuse of cryptographic material.
