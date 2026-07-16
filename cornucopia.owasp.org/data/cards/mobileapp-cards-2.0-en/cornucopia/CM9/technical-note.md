## Technical Note: Alessandro can exploit the app by taking advantage of buffer overflows and memory leaks to write foreign code within the mobile code's address space

### Platform Guidance

**Android:** If the mobile app ships native parsing or media code, fuzz it and compile it with hardening options; memory-unsafe helpers are generous with surprises.

```kotlin
externalNativeBuild {
cmake {
    cppFlags += listOf("-fstack-protector-strong", "-D_FORTIFY_SOURCE=2")
}
}
```

**iOS:** Audit Swift/Objective-C bridges to C libraries, fuzz complex inputs, and let sanitizers embarrass the bugs before attackers do.

```swift
ENABLE_ADDRESS_SANITIZER = YES
ENABLE_UNDEFINED_BEHAVIOR_SANITIZER = YES
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0043, MASTG-TEST-0086
**New Tests:** MASTG-TEST-0337, MASTG-TEST-0399, MASTG-TEST-0384

### MASWE Weaknesses

- MASWE-0080, MASWE-0088: buffer overflow, memory corruption, and leak weaknesses in mobile code.
