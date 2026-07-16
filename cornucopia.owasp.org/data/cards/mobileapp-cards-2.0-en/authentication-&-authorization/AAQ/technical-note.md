## Technical Note: Riotaro can inject and run a command that the application will run at a higher privilege level without being authenticated or authorized to do so

### Platform Guidance

**Android:** Do not let unauthenticated callers trigger privileged code paths via exported services, shell-style commands, or debug helpers.

```kotlin
override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
enforceCallingPermission("com.example.ADMIN_ONLY", "permission required")
return START_NOT_STICKY
}
```

**iOS:** Keep privileged operations behind authenticated app state and reject command-style URL actions unless the caller and the request are both authorized.

```swift
guard session.isAuthenticated, request.command == .rotateKeys else {
throw AuthorizationError.denied
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0033, MASTG-TEST-0025, MASTG-TEST-0078
**New Tests:** MASTG-TEST-0271

### MASWE Weaknesses

- MASWE-0037: command execution and privilege misuse without proper authentication or authorization.
