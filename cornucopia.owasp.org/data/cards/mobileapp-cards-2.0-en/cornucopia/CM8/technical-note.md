## Technical Note: Roxana can do arbitrary file overwrites and potentially execute malicious code through path traversal because the target path and directory is not appropriately validated

### Platform Guidance

**Android:** Normalize file paths before writing and keep overwrite targets inside app-owned directories only.

```kotlin
val base = context.cacheDir.toPath().normalize()
val output = base.resolve(fileName).normalize()
require(output.startsWith(base))
Files.write(output, bytes)
```

**iOS:** Reject `..`, absolute paths, and symlink escapes before writing imported content into the app container.

```swift
let allowedRoot = FileManager.default.temporaryDirectory.standardizedFileURL
let candidate = allowedRoot.appendingPathComponent(fileName).standardizedFileURL
guard candidate.path.hasPrefix(allowedRoot.path) else { throw StorageError.invalidPath }
```

### Relevant Tests

**Legacy Tests:** -
**New Tests:** MASTG-TEST-0287, MASTG-TEST-0300

### MASWE Weaknesses

- : path traversal and arbitrary overwrite issues in storage handling.
