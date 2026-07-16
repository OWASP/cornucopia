## Platform-Aware Review Guidance

**Android**
- Grep source for `addJavascriptInterface`: audit every annotated class and method for access to sensitive resources.
- Restrict bridge availability: check that the loaded URL is on an allowlist before injecting the interface.
- Remove via `webView.removeJavascriptInterface("name")` before loading any content from external sources.
- `WebMessagePort` / `postMessage`: validate the origin before processing the message payload.

**iOS**
- `WKScriptMessageHandler.userContentController(_:didReceive:)` receives messages from all JavaScript in the WebView.
- Validate `message.frameInfo.request.url` against an allowlist before acting on `message.body`.
- Use `WKContentWorld` (iOS 14+) to isolate page scripts from injected bridge scripts.
- Avoid exposing Swift objects to page JavaScript; pass only the minimum required data via `evaluateJavaScript`.

**Testing**
- List all `addJavascriptInterface` calls and their exposed method signatures using static analysis (jadx, semgrep).
- Call all bridge methods from a test WebView with boundary-case and injection inputs.
- Monitor `logcat` during a session with a controlled malicious page for unexpected bridge invocations.

**OWASP Mappings**
- MASVS: PLATFORM-1, PLATFORM-2, STORAGE-2
- MASTG: TEST-0007, TEST-0030, TEST-0033, TEST-0056, TEST-0072, TEST-0078
- MASWE: MASWE-0068
