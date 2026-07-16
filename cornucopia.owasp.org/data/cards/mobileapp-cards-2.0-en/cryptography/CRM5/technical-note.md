## Technical Note: Orace can predict the seed value used for generating cryptographic keys thereby compromising the cryptographic key

### Platform Guidance

**Android:** Use `SecureRandom` or Keystore-generated keys; never seed crypto from timestamps, device IDs, or other values an attacker can guess on a sleepy Tuesday.

```kotlin
val random = SecureRandom()
val keyBytes = ByteArray(32).also(random::nextBytes)
```

**iOS:** Rely on `SecRandomCopyBytes` or system key generation instead of predictable seeds or application-derived entropy.

```swift
var bytes = [UInt8](repeating: 0, count: 32)
SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0016, MASTG-TEST-0063
**New Tests:** MASTG-TEST-0212, MASTG-TEST-0214

### MASWE Weaknesses

- MASWE-0012, MASWE-0025: predictable randomness and poor entropy for cryptographic operations.
