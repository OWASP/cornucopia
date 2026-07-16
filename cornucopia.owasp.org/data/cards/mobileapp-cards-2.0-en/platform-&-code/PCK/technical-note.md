## Technical Note: Grant can modify or expose data by influencing or altering JavaScript bridges, extensions or interprocess communication (e.g. shared memory, message passing, pipes, sockets)

### Platform Guidance

**Android:** Expose only narrowly scoped JavaScript interfaces, require user interaction for dangerous actions, and remove any bridge that does not have a business reason to exist.

```kotlin
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(ReadOnlyBridge(), "SafeBridge")

class ReadOnlyBridge {
@JavascriptInterface fun version(): String = BuildConfig.VERSION_NAME
}
```

**iOS:** Use `WKScriptMessageHandler` with strict message schemas and separate message names for read-only versus state-changing operations.

```swift
final class Bridge: NSObject, WKScriptMessageHandler {
func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
    guard message.name == "safeBridge",
          let body = message.body as? [String: String],
          body["command"] == "version" else { return }
}
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0007, MASTG-TEST-0030, MASTG-TEST-0033, MASTG-TEST-0056, MASTG-TEST-0072, MASTG-TEST-0078
**New Tests:** MASTG-TEST-0292, MASTG-TEST-0355, MASTG-TEST-0394, MASTG-TEST-0332, MASTG-TEST-0376

### MASWE Weaknesses

- MASWE-0060, MASWE-0069: JavaScript bridge and IPC tampering weaknesses that expose privileged functionality.
