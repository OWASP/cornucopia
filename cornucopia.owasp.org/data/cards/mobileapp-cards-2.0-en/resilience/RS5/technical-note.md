## Technical Note: Matteo can bypass access controls and trigger functionality because debugging is left enabled in the production build

### Platform Guidance

**Android:** Ensure `android:debuggable` is false in release, and audit manifest merges so no helpful library re-enables it at the worst possible time.

```kotlin
<application
android:debuggable="false"
tools:replace="android:debuggable" />
```

**iOS:** Ship without development debugging hooks, test menus, or LLDB-friendly shortcuts compiled into production.

```swift
#if !DEBUG
assert(!_isDebugAssertConfiguration())
#endif
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0039, MASTG-TEST-0082
**New Tests:** MASTG-TEST-0227, MASTG-TEST-0368, MASTG-TEST-0391

### MASWE Weaknesses

- MASWE-0090, MASWE-0104: production debugging exposure that weakens access control or feature gating.
