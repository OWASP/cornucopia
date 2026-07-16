## Technical Note: Prasad can bypass the centralized authentication and authorization controls since they are not being used comprehensively on all interactions

### Platform Guidance

**Android:** Route every sensitive action through a shared authorization component so one forgotten fragment does not become the company's easiest backdoor.

```kotlin
class AuthzInterceptor(private val policy: PolicyEngine) {
fun require(scope: String) {
    check(policy.allows(scope)) { "authorization denied" }
}
}
```

**iOS:** Centralize authorization in a reusable policy layer or API client wrapper instead of sprinkling ad-hoc `if isAdmin` confetti across controllers.

```swift
struct PolicyGuard {
func require(_ permission: Permission) throws {
    guard session.permissions.contains(permission) else { throw AuthorizationError.denied }
}
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0017, MASTG-TEST-0064
**New Tests:** MASTG-TEST-0269

### MASWE Weaknesses

- MASWE-0035: incomplete use of centralized authentication and authorization controls.
