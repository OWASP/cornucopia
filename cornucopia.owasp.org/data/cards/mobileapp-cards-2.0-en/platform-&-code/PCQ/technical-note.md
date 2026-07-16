## Platform-Aware Review Guidance

**Android WebView**
- `WebSettings.setSafeBrowsingEnabled(true)` — verify it has not been disabled.
- `WebSettings.setAllowFileAccess(false)`, `setAllowContentAccess(false)`, `setAllowFileAccessFromFileURLs(false)`, `setAllowUniversalAccessFromFileURLs(false)`.
- Audit every `addJavascriptInterface` call; remove in production or restrict to the minimum needed methods with input validation.
- Deep-link URL validation before `webView.loadUrl()`: parse the `Uri`, verify `scheme` and `host` against an allowlist; reject `javascript:`, `file:`, and `data:` schemes unconditionally.

**iOS WKWebView**
- Implement `decidePolicyFor navigationAction` in `WKNavigationDelegate`: allow only `https://` with allowlisted hostnames.
- Validate Universal Link paths against the `apple-app-site-association` configuration.
- `WKScriptMessageHandler` (equivalent of JS interface): validate all messages; expose only the minimum required methods.
- Use `WKContentWorld` (iOS 14+) to isolate injected scripts from page JavaScript.

**Testing**
- Enumerate all deep-link schemes in `AndroidManifest.xml` and `CFBundleURLTypes`.
- Send crafted deep links with `javascript:`, `file://`, and attacker-controlled `https://` URLs; verify all are rejected.
- Use Frida to hook `WebView.loadUrl()` and log all URLs loaded during a session.

**OWASP Mappings**
- MASVS: AUTH-1, CODE-4, PLATFORM-1, PLATFORM-2, STORAGE-2
- MASTG: TEST-0027, TEST-0028, TEST-0031, TEST-0032, TEST-0033, TEST-0070, TEST-0075, TEST-0076, TEST-0077, TEST-0078, TEST-0250, TEST-0251, TEST-0252, TEST-0253, TEST-0331, TEST-0332, TEST-0333, TEST-0334, TEST-0335, TEST-0336, TEST-0370, TEST-0371, TEST-0376, TEST-0377, TEST-0378, TEST-0379, TEST-0380, TEST-0393, TEST-0394, TEST-0395, TEST-0398, TEST-0399, TEST-0400
- MASWE: MASWE-0040, MASWE-0058, MASWE-0069, MASWE-0070, MASWE-0071, MASWE-0072, MASWE-0073
