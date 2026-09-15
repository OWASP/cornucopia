## Scenario: Fady can bypass cryptographic controls because they do not fail securely (i.e. they default to unprotected)

### Example

Fady sends a sealed message through an app while the encryption service is unavailable. Instead of refusing to send, the app quietly posts the text in a public group, where everyone learns that Fady’s surprise party is “definitely not for Brenda.”

Security failure must fail closed, not fall back to unprotected data. An unavailable cryptographic control should stop the sensitive operation and report a safe, generic error.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Tampering**, **Elevation of Privilege** in STRIDE. The named condition is: Fady can bypass cryptographic controls because they do not fail securely (i.e. they default to unprotected).

- **MAS-THREAT-0027:** Attackers can intercept or modify TLS-protected network traffic.

- **MAS-ATTACK-0014:** Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point.
- **MAS-ATTACK-0015:** Presenting a fraudulent or otherwise invalid certificate that the app accepts.

### What can go wrong?

If Fady can bypass cryptographic controls because they do not fail securely (i.e. they default to unprotected), the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point. Also, Presenting a fraudulent or otherwise invalid certificate that the app accepts. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0027 — Insecure Certificate Validation: This weakness occurs when an app does not properly validate TLS certificates during secure communication, accepting invalid, expired, self-signed, or untrusted certificates without appropriate verification.

### What are we going to do about it?

Make every cryptographic failure fail closed: return no plaintext or unauthenticated result, use uniform error handling, and test malformed, expired, and tampered inputs so exceptions cannot downgrade the operation to an unprotected path.


Mapped MASTG tests:

- MASTG-TEST-0282 — Unsafe Custom Trust Evaluation: This test evaluates whether an Android app uses `checkServerTrusted(...)` in an unsafe manner as part of a custom `TrustManager`, causing any connection configured to use that `TrustManager` to skip certificate validation.
- MASTG-TEST-0283 — Incorrect Implementation of Server Hostname Verification: This test evaluates whether an Android app implements a `HostnameVerifier` that uses `verify(...)`) in an unsafe manner, effectively turning off hostname validation for the affected connections.
- MASTG-TEST-0284 — Incorrect SSL Error Handling in WebViews: This test evaluates whether an Android app has WebViews that ignore SSL/TLS certificate errors by overriding the `onReceivedSslError(...)` method without proper validation.
- MASTG-TEST-0396 — References to URLSessionDelegate Bypassing Certificate Validation: iOS apps that use `URLSession` can optionally override the system's default server trust evaluation by implementing `urlSession(_:didReceive:completionHandler:)` from `URLSessionDelegate` (session-level) or...
- MASTG-TEST-0397 — References to WKNavigationDelegate Bypassing Certificate Validation: `WKWebView` handles server authentication challenges through `WKNavigationDelegate.webView(_:didReceive:completionHandler:)`. When the app provides a navigation delegate that implements this method, the WebView's default certificate...

Mapped MASTG best practices:

- MASTG-BEST-0021 — Ensure Proper Error and Exception Handling: Secure exception and error handling in Android is about preventing the leakage of sensitive information, managing failures gracefully, and ensuring that errors do not compromise security. User-facing error messages should remain...
- MASTG-BEST-0073 — Properly Validate Server Trust in URLSessionDelegate and WKNavigationDelegate: When an iOS app overrides the default certificate validation by implementing `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)`) or `WKNavigationDelegate.webView(_:didReceive:completionHandler:)`), it takes full control of...

Mapped MASTG knowledge:

- MASTG-KNOW-0010 — Exception Handling: Exceptions occur when an application gets into an abnormal or error state. Both Java and C++ may throw exceptions. Testing exception handling is about ensuring that the app will handle an exception and transition to a safe state without...
- MASTG-KNOW-0072 — Server Trust Evaluation: ATS imposes extended security checks that supplement the default server trust evaluation prescribed by the Transport Layer Security (TLS) protocol. Loosening ATS restrictions reduces the security of the app. Apps should prefer...
