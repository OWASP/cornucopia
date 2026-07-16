## Technical Note: Simon can bypass hashing and encryption functions because they are custom and/or inadequately implemented

### Platform Guidance

**Android:** Do not invent hash or cipher schemes in application code; the only acceptable custom crypto is the story you tell later about why you removed it.

```kotlin
val digest = MessageDigest.getInstance("SHA-256").digest(data)
```

**iOS:** Use standard KDFs, MACs, and ciphers rather than bespoke combinations that only one former developer understands.

```swift
let digest = SHA256.hash(data: data)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0014, MASTG-TEST-0061
**New Tests:** MASTG-TEST-0312

### MASWE Weaknesses

- MASWE-0019: custom cryptographic implementations and inadequate primitive composition.
