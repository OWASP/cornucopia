## Technical Note: Xavier can inject scripts into the web view because it allows embedding content using deep linking without proper authorization and validation of the host, schema and path of the target as these can be changed by the user or because safe browsing is disabled

### Platform Guidance

**Android:** Keep WebView navigation behind an allowlist of schemes, hosts, and paths, and enable Safe Browsing for untrusted content.

```kotlin
val allowedHosts = setOf("example.com")
webView.webViewClient = object : WebViewClient() {
override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
    val url = request.url
    return !(url.scheme == "https" && url.host in allowedHosts)
}
}
WebView.setSafeBrowsingEnabled(true)
```

**iOS:** In `WKWebView`, use app-bound domains or a navigation delegate to block hostile deep links and script-capable surprise detours.

```swift
let allowedHosts = Set(["example.com"])
func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
let url = action.request.url
if url?.scheme == "https" && url?.host.map(allowedHosts.contains) == true {
    decisionHandler(.allow)
} else {
    decisionHandler(.cancel)
}
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0027, MASTG-TEST-0028, MASTG-TEST-0031, MASTG-TEST-0070, MASTG-TEST-0076, MASTG-TEST-0077
**New Tests:** MASTG-TEST-0291, MASTG-TEST-0340, MASTG-TEST-0393, MASTG-TEST-0331, MASTG-TEST-0371, MASTG-TEST-0395

### MASWE Weaknesses

- MASWE-0059, MASWE-0068, MASWE-0119: deep link and WebView trust-boundary failures that enable script injection or content confusion.
