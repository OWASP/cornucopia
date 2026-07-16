## Technical Note: Adel can predict and use the app's cryptographic keys because they are insufficiently long and random, can be enumerated, or derived from known values

### Platform Guidance

**Android:** Pick key sizes and curves that meet current recommendations and let the platform generate them with real entropy.

```kotlin
val spec = KeyGenParameterSpec.Builder("ec-key", KeyProperties.PURPOSE_SIGN)
.setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1"))
.build()
```

**iOS:** Use CryptoKit defaults or explicitly selected modern parameters rather than short keys, legacy curves, or derived values with obvious structure.

```swift
let key = P256.Signing.PrivateKey()
let sharedSecret = try P256.KeyAgreement.PrivateKey().sharedSecretFromKeyAgreement(with: peerKey)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0013, MASTG-TEST-0016, MASTG-TEST-0063
**New Tests:** MASTG-TEST-0307, MASTG-TEST-0349

### MASWE Weaknesses

- MASWE-0015: weak key length, poor randomness, or guessable derivation inputs.
