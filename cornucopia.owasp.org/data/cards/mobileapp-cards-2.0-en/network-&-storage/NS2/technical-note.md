## Technical Note: Matt can inspect sensitive application log data because logging statements have not been removed or reviewed as safe before the production release

### Platform Guidance

**Android:** Never log secrets, tokens, PANs, or health data; build redaction into the logger so developers do not have to remember it during each caffeinated sprint.

```kotlin
class RedactingLogger {
fun info(message: String) = Log.i("app", message.replace(Regex("token=[^&\s]+"), "token=<redacted>"))
}
```

**iOS:** Use `Logger` privacy annotations and keep release logging intentionally boring.

```swift
import OSLog
let logger = Logger(subsystem: "org.example.app", category: "auth")
logger.info("login for user=\(userId, privacy: .private(mask: .hash))")
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0003, MASTG-TEST-0053
**New Tests:** MASTG-TEST-0200, MASTG-TEST-0304, MASTG-TEST-0301

### MASWE Weaknesses

- MASWE-0001: storage and disclosure weaknesses caused by sensitive data ending up in application logs.
