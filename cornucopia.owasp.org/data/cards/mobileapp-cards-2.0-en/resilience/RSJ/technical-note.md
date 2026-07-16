## Technical Note: Pekka can compromise the integrity of the storage because the file integrity checks aren't strong enough according to what is recommended or the perceived effort of a potential attacker

### Platform Guidance

**Android:** Store integrity metadata separately, verify it before use, and sign manifests or local databases so tampering is obvious.

```kotlin
val expected = metadata.expectedHash(fileName)
val actual = file.inputStream().use { sha256(it) }
require(actual == expected)
```

**iOS:** Use signed manifests or authenticated encryption for local files so a modified blob fails validation before parsing.

```swift
let actual = SHA256.hash(data: fileData)
guard Data(actual) == expectedHash else { throw IntegrityError.modified }
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0047, MASTG-TEST-0090
**New Tests:** MASTG-TEST-0288, MASTG-TEST-0246

### MASWE Weaknesses

- MASWE-0096: weak file-integrity verification for local storage or cached content.
