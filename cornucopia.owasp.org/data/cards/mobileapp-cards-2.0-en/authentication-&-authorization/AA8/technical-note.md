## Technical Note: Pramod can intercept credentials through misdirection because the app is vulnerable to attacks like Tapjacking, StrandHogg and/or URL scheme hijacking

### Platform Guidance

**Android:** Block overlay attacks with `setFilterTouchesWhenObscured(true)`, mark sensitive screens as secure, and verify the destination of deep links and scheme handlers.

```kotlin
approveButton.filterTouchesWhenObscured = true
approveButton.setOnTouchListener { _, event ->
(event.flags and MotionEvent.FLAG_WINDOW_IS_OBSCURED) == 0
}
```

**iOS:** Use universal links instead of custom schemes when possible and confirm the host/path before accepting credential-related callbacks.

```swift
guard url.scheme == "https", url.host == "login.example.com" else {
throw AuthError.invalidCallback
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0025, MASTG-TEST-0030, MASTG-TEST-0035, MASTG-TEST-0072, MASTG-TEST-0075
**New Tests:** MASTG-TEST-0267

### MASWE Weaknesses

- MASWE-0033, MASWE-0045: credential interception through overlay, task-hijacking, or URL-handler abuse.
