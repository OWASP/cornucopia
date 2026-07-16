## Technical Note: Enselme can modify sensitive data (stored or in transit) because it is not subject to integrity checking

### Platform Guidance

**Android:** Use authenticated encryption or a detached MAC so the app can detect modified ciphertext before processing it.

```kotlin
val cipher = Cipher.getInstance("AES/GCM/NoPadding")
cipher.init(Cipher.ENCRYPT_MODE, key)
val ciphertext = cipher.doFinal(plaintext)
```

**iOS:** Prefer AEAD modes such as AES-GCM or ChaChaPoly instead of encrypt-only designs that trust integrity to good vibes.

```swift
let box = try ChaChaPoly.seal(data, using: key)
let opened = try ChaChaPoly.open(box, using: key)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0002
**New Tests:** MASTG-TEST-0208, MASTG-TEST-0213

### MASWE Weaknesses

- MASWE-0011, MASWE-0024: missing integrity protection for sensitive stored or transmitted data.
