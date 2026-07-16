## Technical Note: Max can modify or expose data because input validation and sanitation are not properly applied to interprocess communication or because extensions are not properly restricted

### Platform Guidance

**Android:** Use strict schema validation for extras and only allow trusted file extensions or MIME types when accepting shared content.

```kotlin
val allowedTypes = setOf("image/png", "application/pdf")
val type = intent.type ?: error("missing MIME type")
require(type in allowedTypes)
val attachment = intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
```

**iOS:** For share extensions and custom schemes, validate file extension, Uniform Type Identifier, and payload shape before processing.

```swift
let allowed = [UTType.png.identifier, UTType.pdf.identifier]
guard let item = provider.registeredTypeIdentifiers.first, allowed.contains(item) else {
return
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0025, MASTG-TEST-0072
**New Tests:** MASTG-TEST-0245, MASTG-TEST-0382, MASTG-TEST-0273

### MASWE Weaknesses

- MASWE-0077, MASWE-0085: input validation and extension restriction weaknesses in interprocess data handling.
