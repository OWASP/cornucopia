## Technical Note: Lauren can traverse or modify otherwise protected files through access to the underlying file system by exploiting weaknesses in file system-based content providers, resolvers or its configuration

### Platform Guidance

**Android:** Normalize requested paths, refuse traversal sequences, and use a `FileProvider` XML allowlist instead of rolling your own adventurous filesystem tour guide.

```kotlin
val root = context.filesDir.toPath().normalize()
val target = root.resolve(requestedName).normalize()
require(target.startsWith(root)) { "path traversal blocked" }
```

**iOS:** Build file URLs from app-controlled container roots and reject bookmark or path values that escape the intended sandbox location.

```swift
let root = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
let target = root.appendingPathComponent(candidate).standardizedFileURL
guard target.path.hasPrefix(root.path) else { throw StorageError.invalidPath }
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0007, MASTG-TEST-0056
**New Tests:** MASTG-TEST-0258, MASTG-TEST-0320, MASTG-TEST-0366, MASTG-TEST-0280, MASTG-TEST-0347, MASTG-TEST-0389

### MASWE Weaknesses

- MASWE-0057, MASWE-0065, MASWE-0074: path traversal and file-provider weaknesses that let attackers reach protected content.
