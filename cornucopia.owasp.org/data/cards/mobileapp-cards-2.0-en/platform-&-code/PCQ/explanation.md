## Scenario: Xavier can inject scripts into the web view because it allows embedding content using deep linking without proper authorization and validation of the host, schema, and path of the target, or because safe browsing is disabled

Consider a scenario where Xavier discovers the target app's deep-link handler parses a `url` parameter and passes it directly to `WebView.loadUrl()` without any hostname validation. Xavier sends the victim a push notification with the deep link `targetapp://view?url=https://accounts.target-app.com.evil.example/login`. The app opens the URL in a branded WebView, without an address bar, on a page that mimics the real login screen. The user enters their credentials. Xavier's server receives them.

Additionally, the WebView has `addJavascriptInterface` exposing native methods, and `setAllowUniversalAccessFromFileURLs(true)` enabled — so attacker-controlled JavaScript can call native APIs and read local files.

### Example

Xavier sends a crafted deep link through a social media message. The link is `appscheme://open?url=javascript:alert(document.cookie)`. The WebView loads the `javascript:` URL, executes the script, and displays the session cookie in an alert — proving that script injection is possible. The same technique, with a `fetch()` call instead of `alert()`, silently exfiltrates the token to Xavier's server. Safe browsing was disabled after it flagged a test domain during development.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** (script injection), **Spoofing** (phishing via trusted app chrome), and **Elevation of Privilege** (native API access from injected script).

### What can go wrong?

- Injected JavaScript runs in the WebView's origin context, accessing cookies, `localStorage`, and any exposed native bridge methods.
- Without an address bar, users cannot verify the URL, enabling highly convincing phishing.
- `addJavascriptInterface` bridges allow attacker scripts to invoke sensitive device APIs.
- `setAllowFileAccessFromFileURLs` and `setAllowUniversalAccessFromFileURLs` enable cross-origin file reads.

### What are we going to do about it?

- Validate the full URL (scheme, host, path) against an allowlist before passing it to any WebView loading method.
- Enable Safe Browsing: `WebView.setSafeBrowsingEnabled(true)`.
- Remove `addJavascriptInterface` from release builds, or restrict it to a minimal, hardened API surface with input validation.
- Disable unnecessary WebView settings: `setAllowFileAccessFromFileURLs(false)`, `setAllowUniversalAccessFromFileURLs(false)`.
- On iOS, implement `WKNavigationDelegate` to allow only allowlisted origins.
