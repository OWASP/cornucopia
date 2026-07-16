## Technical Note: Jason can provoke memory leak or corruption because the app has cyclic dependencies, manages pointers inadequately, keeps an incorrect reference count, does not release shared resources or apply stack protection

### Platform Guidance

**Android:** If the app ships native code, compile it with modern hardening flags and review ownership boundaries between Java/Kotlin and JNI objects.

```kotlin
android {
defaultConfig {
    externalNativeBuild {
        cmake {
            cppFlags += listOf(
                "-D_FORTIFY_SOURCE=2",
                "-fstack-protector-strong",
                "-fPIE"
            )
        }
    }
}
}
```

**iOS:** Prefer ARC-safe Swift over manual memory management, and enable Address Sanitizer and stack protection in debug pipelines for native modules.

```swift
OTHER_CFLAGS = $(inherited) -fstack-protector-strong
OTHER_SWIFT_FLAGS = $(inherited) -sanitize=address
ENABLE_HARDENED_RUNTIME = YES
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0043, MASTG-TEST-0044, MASTG-TEST-0086
**New Tests:** MASTG-TEST-0222, MASTG-TEST-0374, MASTG-TEST-0229

### MASWE Weaknesses

- MASWE-0075, MASWE-0083: memory safety, lifetime management, and native-code defects that lead to corruption or code execution.
