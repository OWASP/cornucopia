## Technical Note: Carlos can use the application's notification services to launch phishing campaigns because notifications are not sanitized and validated according to best practices

### Platform Guidance

**Android:** Sanitize notification content, use immutable pending intents, and never let remote text impersonate trusted app actions or brands.

```kotlin
val safeBody = Html.escapeHtml(messagePreview)
NotificationCompat.Builder(this, CHANNEL)
.setContentText(safeBody)
.setContentIntent(safePendingIntent)
```

**iOS:** Keep push payloads and local notifications free of attacker-controlled formatting or links that bypass the app's normal trust checks.

```swift
content.body = messagePreview.replacingOccurrences(of: "
", with: " ")
content.userInfo = ["messageId": messageId]
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0025, MASTG-TEST-0072
**New Tests:** MASTG-TEST-0339, MASTG-TEST-0400, MASTG-TEST-0386

### MASWE Weaknesses

- MASWE-0081, MASWE-0116: notification phishing and injection through unsanitized message channels.
