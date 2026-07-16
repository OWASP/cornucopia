## Technical Note: Fady can bypass cryptographic controls because they do not fail securely (i.e. they default to unprotected)

### Platform Guidance

**Android:** If decrypt or verify fails, stop the workflow and surface a safe error instead of continuing as if the ciphertext merely had a personality.

```kotlin
return runCatching { aead.decrypt(blob, aad) }
.getOrElse { throw SecurityException("ciphertext validation failed") }
```

**iOS:** Treat cryptographic failures as hard security failures, not optional warnings or opportunities to keep processing corrupted data.

```swift
do {
_ = try AES.GCM.open(box, using: key)
} catch {
throw CryptoError.validationFailed
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0014
**New Tests:** MASTG-TEST-0308

### MASWE Weaknesses

- MASWE-0016: fail-open cryptographic error handling.
