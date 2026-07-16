## Technical Note: Tobias can disclose sensitive data by dumping debug symbols while the application is running

### Platform Guidance

**Android:** Do not ship symbol-rich debug artifacts with the production APK/AAB, and store mapping files separately for incident response.

```kotlin
buildTypes {
release {
    ndk { debugSymbolLevel = "NONE" }
}
}
```

**iOS:** Generate dSYMs for crash processing but do not expose them through app bundles or public artifact stores.

```swift
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym
STRIP_INSTALLED_PRODUCT = YES
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0040, MASTG-TEST-0083
**New Tests:** MASTG-TEST-0225, MASTG-TEST-0352, MASTG-TEST-0367

### MASWE Weaknesses

- MASWE-0067, MASWE-0102: debug symbol exposure that helps reverse engineers understand sensitive logic.
