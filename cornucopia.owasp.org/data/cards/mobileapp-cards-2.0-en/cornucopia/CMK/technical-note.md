## Technical Note: Ruben can use the app, without modifications, to spread malicious code because methods for transfer and storage do not perform proper data sanitization and validation

### Platform Guidance

**Android:** Sanitize files, messages, and packages before forwarding them so the app does not become an unwilling malware courier with a nice icon.

```kotlin
val safeName = inputName.replace(Regex("[^A-Za-z0-9._-]"), "_")
require(mimeType in allowedMimeTypes)
```

**iOS:** Apply type allowlists, content validation, and safe filename handling before data leaves the app or is reimported elsewhere.

```swift
let safeName = originalName.replacingOccurrences(of: "[^A-Za-z0-9._-]", with: "_", options: .regularExpression)
guard allowedTypes.contains(contentType) else { throw ValidationError.unsupportedType }
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0047, MASTG-TEST-0090
**New Tests:** MASTG-TEST-0341, MASTG-TEST-0358

### MASWE Weaknesses

- MASWE-0100: sanitization weaknesses in transfer and storage paths that could propagate malicious content.
