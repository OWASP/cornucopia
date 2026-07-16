## Technical Note: Ash can break the cryptography because it is not strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Use recommended algorithms and modes such as AES-GCM, ChaCha20-Poly1305, P-256, and SHA-256 rather than legacy primitives.

```kotlin
val cipher = Cipher.getInstance("AES/GCM/NoPadding")
val mac = Mac.getInstance("HmacSHA256")
```

**iOS:** CryptoKit gives you good defaults; the fact that a weaker primitive still compiles is not a product requirement.

```swift
let key = SymmetricKey(size: .bits256)
let tag = HMAC<SHA256>.authenticationCode(for: data, using: key)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0014, MASTG-TEST-0061
**New Tests:** MASTG-TEST-0309

### MASWE Weaknesses

- MASWE-0017: use of outdated, weak, or poorly chosen cryptographic primitives.
