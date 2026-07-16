## Technical Note: Tarik can influence or alter cryptographic operations and can therefore bypass them

### Platform Guidance

**Android:** Protect keys, algorithm choices, and crypto parameters from tampering and confirm on the server that signed or encrypted data came from a trusted client state.

```kotlin
val protectedConfig = verifySignedConfig(remoteConfigBytes, configSignature)
require(protectedConfig.alg == "AES_GCM")
```

**iOS:** Treat crypto configuration as signed policy data, not a user-editable suggestion that decides how trustworthy ciphertext should be today.

```swift
guard config.signatureValid, config.algorithm == .aesGCM else {
throw CryptoError.invalidConfiguration
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0014, MASTG-TEST-0061, MASTG-TEST-0062
**New Tests:** MASTG-TEST-0350

### MASWE Weaknesses

- MASWE-0020: tampering with cryptographic operations, parameters, or trust decisions.
