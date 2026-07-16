## Technical Note: Gastón can execute malicious actions through intent redirection because the intent is not properly sanitized and immutable

### Platform Guidance

**Android:** Use immutable `PendingIntent`s, sanitize nested intents, and refuse to forward attacker-controlled extras into privileged destinations.

```kotlin
val pending = PendingIntent.getActivity(
context, 0, Intent(context, SafeActivity::class.java),
PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
)
```

**iOS:** For equivalent hand-off flows on iOS, validate route parameters before dispatching navigation or privileged extension actions.

```swift
guard route.host == "trusted-action",
  route.queryItems["target"] == "inbox" else { return }
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0025, MASTG-TEST-0030, MASTG-TEST-0072
**New Tests:** MASTG-TEST-0274, MASTG-TEST-0398, MASTG-TEST-0383

### MASWE Weaknesses

- MASWE-0079, MASWE-0087: intent redirection, mutable-payload handling, and IPC sanitization gaps.
