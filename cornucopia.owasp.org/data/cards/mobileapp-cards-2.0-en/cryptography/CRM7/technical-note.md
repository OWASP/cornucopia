## Technical Note: Ramsey can access stored sensitive data because it is not securely encrypted

### Platform Guidance

**Android:** Encrypt sensitive files and database fields with modern algorithms and app-specific keys before writing them to storage.

```kotlin
val encryptedFile = EncryptedFile.Builder(
context, secretFile, masterKey, EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
).build()
```

**iOS:** Combine Data Protection with strong application-layer encryption where the data value and threat model require it.

```swift
let sealed = try AES.GCM.seal(recordData, using: key)
try sealed.combined?.write(to: fileURL, options: .completeFileProtection)
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0001, MASTG-TEST-0013, MASTG-TEST-0052, MASTG-TEST-0062
**New Tests:** MASTG-TEST-0232, MASTG-TEST-0317

### MASWE Weaknesses

- MASWE-0014, MASWE-0027: weak or missing encryption for sensitive data at rest.
