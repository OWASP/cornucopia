## Technical Note: Taher can intercept, extract or modify sensitive data at rest or in transit by influencing or altering methods for transferring or storing data at rest or in transit

### Platform Guidance

**Android:** Authenticate and integrity-protect data both at rest and in transit so an attacker cannot rewrite storage helpers or sync payloads without detection.

```kotlin
val ciphertext = aead.encrypt(plaintext, associatedData)
val restored = aead.decrypt(ciphertext, associatedData)
```

**iOS:** Use authenticated encryption or message authentication around storage and sync formats; checksums alone are a polite suggestion to attackers.

```swift
let sealed = try AES.GCM.seal(data, using: key)
let opened = try AES.GCM.open(sealed, using: key)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0001, MASTG-TEST-0052
**New Tests:** MASTG-TEST-0262, MASTG-TEST-0299

### MASWE Weaknesses

- : tampering with storage or transfer mechanisms that handle sensitive data.
