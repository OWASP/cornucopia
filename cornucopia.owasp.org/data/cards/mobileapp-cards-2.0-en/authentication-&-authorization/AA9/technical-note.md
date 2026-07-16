## Technical Note: Wong can bypass the authentication because it does not fail securely. (i.e. it defaults to allowing unauthenticated access)

### Platform Guidance

**Android:** When auth state is unknown, expired, or broken, default to denial and force reauthentication rather than letting the app improvise optimism.

```kotlin
val session = sessionStore.current() ?: return showLogin()
if (!session.isValid()) return showLogin()
openDashboard()
```

**iOS:** Return the user to a safe locked state on every authentication error path, including biometric cancellation, token parse failures, or missing policy objects.

```swift
guard let session = sessionStore.current, session.isValid else {
presentLogin()
return
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0017, MASTG-TEST-0018, MASTG-TEST-0064
**New Tests:** MASTG-TEST-0268

### MASWE Weaknesses

- MASWE-0034, MASWE-0046: fail-open authentication paths and insecure defaults when checks error out.
