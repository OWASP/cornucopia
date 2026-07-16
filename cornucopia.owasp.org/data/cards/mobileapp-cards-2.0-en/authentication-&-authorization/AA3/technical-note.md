## Technical Note: Choi can access capabilities, objects, resources, or properties they should not be authorized to access because entitlements or permissions are too wide, not properly set or not enforced

### Platform Guidance

**Android:** Treat permissions and roles as server-verifiable authorization facts; exported activities and custom permissions should be scoped to the minimum access pattern.

```kotlin
<activity
android:name=".AdminActivity"
android:exported="false"
android:permission="com.example.ADMIN_ONLY" />
```

**iOS:** Keep entitlements narrow, validate authorization decisions on the backend, and avoid client-only role checks in feature flags.

```swift
guard currentUser.roles.contains(.admin) else {
throw AuthorizationError.denied
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0024, MASTG-TEST-0032, MASTG-TEST-0069, MASTG-TEST-0077
**New Tests:** MASTG-TEST-0327

### MASWE Weaknesses

- MASWE-0028, MASWE-0040: authorization scope, entitlements, and overbroad capability assignment.
