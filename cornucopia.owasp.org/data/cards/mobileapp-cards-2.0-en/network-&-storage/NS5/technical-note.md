## Technical Note: Kevin can read sensitive data mapped to user accounts or sessions by extracting data sent through third-party libraries and/or notifications sent between the app and embedded services (e.g. logs, notifications, backups, cache, local db)

### Platform Guidance

**Android:** Review every SDK, notification payload, cache, and analytics event for tenant separation and secret minimization before it leaves the process.

```kotlin
val notification = NotificationCompat.Builder(this, CHANNEL)
.setContentTitle("New message")
.setContentText("Open the app to view details")
.setVisibility(NotificationCompat.VISIBILITY_PRIVATE)
.build()
```

**iOS:** Avoid putting account secrets into push payloads, extension storage, or third-party telemetry libraries; send opaque identifiers and fetch details after unlock.

```swift
let content = UNMutableNotificationContent()
content.title = "New message"
content.body = "Unlock the app to read it."
content.userInfo = ["messageId": message.id]
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0004, MASTG-TEST-0005, MASTG-TEST-0054
**New Tests:** MASTG-TEST-0203, MASTG-TEST-0215, MASTG-TEST-0313

### MASWE Weaknesses

- MASWE-0004: leakage through SDKs, notifications, caches, and other side channels mapped to user accounts.
