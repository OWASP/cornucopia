## Technical Note: Sebastien can disclose sensitive data because the application is set up to log debug information at runtime

### Platform Guidance

**Android:** Strip debug logging from release builds and gate extra diagnostics behind developer-only flags that are not enabled in production.

```kotlin
buildTypes {
release {
    buildConfigField("boolean", "DEBUG_LOGGING", "false")
    minifyEnabled true
}
}
```

**iOS:** Compile release builds with lightweight operational logs only and keep verbose traces out of shipping binaries.

```swift
#if DEBUG
logger.debug("token exchange trace: \(traceId)")
#endif
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0041, MASTG-TEST-0084
**New Tests:** MASTG-TEST-0224, MASTG-TEST-0351, MASTG-TEST-0359

### MASWE Weaknesses

- MASWE-0008, MASWE-0101: runtime debug logging and exposure of sensitive internals to an attacker.
