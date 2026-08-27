## Scenario: Enselme can modify sensitive data (stored or in transit) because it is not subject to integrity checking

### Example

Enselme sells concert tickets through an app that stores the price and seat number without a signature. A prankster changes the price to one cent and seat 1A, leaving the band to discover that the front row is occupied by a very pleased accountant.

Sensitive data needs an integrity check that detects alteration in storage or transit. Without authenticated protection, the recipient cannot tell whether the ticket or transaction was changed by an intermediary.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Elevation of Privilege** in STRIDE. The named condition is: Enselme can modify sensitive data (stored or in transit) because it is not subject to integrity checking.

- **MAS-THREAT-0057:** Attackers can alter the app's behavior through its resources.
- **MAS-THREAT-0027:** Attackers can intercept or modify TLS-protected network traffic.

- **MAS-ATTACK-0009:** Tampering with backup contents and restoring the modified backup to a device.
- **MAS-ATTACK-0070:** Modifying the app's files or resources on a compromised device.
- **MAS-ATTACK-0014:** Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point.
- **MAS-ATTACK-0015:** Presenting a fraudulent or otherwise invalid certificate that the app accepts.

### What can go wrong?

If Enselme can modify sensitive data (stored or in transit) because it is not subject to integrity checking, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cryptography boundary and reach data or capability that this flow should protect. In this card, the practical route includes Tampering with backup contents and restoring the modified backup to a device. Also, Modifying the app's files or resources on a compromised device. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0057 — App Resources Integrity Not Verified: This weakness occurs when an app does not verify that the resources it relies on have not been tampered with.
- MASWE-0027 — Insecure Certificate Validation: This weakness occurs when an app does not properly validate TLS certificates during secure communication, accepting invalid, expired, self-signed, or untrusted certificates without appropriate verification.

### What are we going to do about it?

Authenticate every sensitive record and message with AEAD, an encrypt-then-MAC construction, or a digital signature; verify tags before parsing or using data and test modified ciphertext, signatures, and error paths.


Mapped MASTG tests:

- MASTG-TEST-0338 — References to Storage Integrity Check APIs: Android apps can protect the integrity and authenticity of data they store on the device (e.g., in `SharedPreferences`, files, or databases) by computing an HMAC or a digital signature over the data and verifying it before use (see...
- MASTG-TEST-0234 — Missing Implementation of Server Hostname Verification with SSLSockets: This test checks whether an Android app uses `SSLSocket` without a `HostnameVerifier`, allowing connections to servers presenting certificates with **wrong or invalid hostnames**.
- MASTG-TEST-0282 — Unsafe Custom Trust Evaluation: This test evaluates whether an Android app uses `checkServerTrusted(...)` in an unsafe manner as part of a custom `TrustManager`, causing any connection configured to use that `TrustManager` to skip certificate validation.
- MASTG-TEST-0283 — Incorrect Implementation of Server Hostname Verification: This test evaluates whether an Android app implements a `HostnameVerifier` that uses `verify(...)`) in an unsafe manner, effectively turning off hostname validation for the affected connections.
- MASTG-TEST-0284 — Incorrect SSL Error Handling in WebViews: This test evaluates whether an Android app has WebViews that ignore SSL/TLS certificate errors by overriding the `onReceivedSslError(...)` method without proper validation.
- MASTG-TEST-0396 — References to URLSessionDelegate Bypassing Certificate Validation: iOS apps that use `URLSession` can optionally override the system's default server trust evaluation by implementing `urlSession(_:didReceive:completionHandler:)` from `URLSessionDelegate` (session-level) or...
- MASTG-TEST-0397 — References to WKNavigationDelegate Bypassing Certificate Validation: `WKWebView` handles server authentication challenges through `WKNavigationDelegate.webView(_:didReceive:completionHandler:)`. When the app provides a navigation delegate that implements this method, the WebView's default certificate...

Mapped MASTG best practices:

- MASTG-BEST-0066 — Implementing Storage Integrity Checks on Android: Implement storage integrity checks in Android apps to detect unauthorized modifications to data stored on the device (for example, in `SharedPreferences`, files, or databases). These checks raise the cost for attackers who try to tamper...
- MASTG-BEST-0021 — Ensure Proper Error and Exception Handling: Secure exception and error handling in Android is about preventing the leakage of sensitive information, managing failures gracefully, and ensuring that errors do not compromise security. User-facing error messages should remain...
- MASTG-BEST-0073 — Properly Validate Server Trust in URLSessionDelegate and WKNavigationDelegate: When an iOS app overrides the default certificate validation by implementing `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)`) or `WKNavigationDelegate.webView(_:didReceive:completionHandler:)`), it takes full control of...

Mapped MASTG knowledge:

- MASTG-KNOW-0036 — Shared Preferences: !!! warning
- MASTG-KNOW-0010 — Exception Handling: Exceptions occur when an application gets into an abnormal or error state. Both Java and C++ may throw exceptions. Testing exception handling is about ensuring that the app will handle an exception and transition to a safe state without...
- MASTG-KNOW-0072 — Server Trust Evaluation: ATS imposes extended security checks that supplement the default server trust evaluation prescribed by the Transport Layer Security (TLS) protocol. Loosening ATS restrictions reduces the security of the app. Apps should prefer...
