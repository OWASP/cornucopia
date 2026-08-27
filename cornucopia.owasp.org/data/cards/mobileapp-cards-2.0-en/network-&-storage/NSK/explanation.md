## Scenario: Maarten can impersonate a trusted server and expose or modify data in transit because TLS certificate, hostname, or custom trust validation is weak or can be bypassed

### Example

Maarten visits a pop-up ticket booth whose app accepts any certificate with a familiar-looking logo. A counterfeit server presents one, rewrites his destination to a village three hours away, and labels the detour “premium sightseeing.”

Certificate, hostname, and custom trust decisions must be independently validated and resistant to bypass. Weak server authentication lets an impostor read or alter supposedly protected traffic.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Tampering**, **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Maarten can impersonate a trusted server and expose or modify data in transit because TLS certificate, hostname, or custom trust validation is weak or can be bypassed.

- **MAS-THREAT-0027:** Attackers can intercept or modify TLS-protected network traffic.

- **MAS-ATTACK-0014:** Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point.
- **MAS-ATTACK-0015:** Presenting a fraudulent or otherwise invalid certificate that the app accepts.

### What can go wrong?

If Maarten can impersonate a trusted server and expose or modify data in transit because TLS certificate, hostname, or custom trust validation is weak or can be bypassed, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point. Also, Presenting a fraudulent or otherwise invalid certificate that the app accepts. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0027 — Insecure Certificate Validation: This weakness occurs when an app does not properly validate TLS certificates during secure communication, accepting invalid, expired, self-signed, or untrusted certificates without appropriate verification.

### What are we going to do about it?

Validate the complete certificate chain and hostname and, where pinning is required, pin a managed certificate or public key with a safe rotation plan; use a proxy and invalid-certificate tests to prove trust-all and bypass paths fail.


Mapped MASTG tests:

- MASTG-TEST-0234 — Missing Implementation of Server Hostname Verification with SSLSockets: This test checks whether an Android app uses `SSLSocket` without a `HostnameVerifier`, allowing connections to servers presenting certificates with **wrong or invalid hostnames**.
- MASTG-TEST-0282 — Unsafe Custom Trust Evaluation: This test evaluates whether an Android app uses `checkServerTrusted(...)` in an unsafe manner as part of a custom `TrustManager`, causing any connection configured to use that `TrustManager` to skip certificate validation.
- MASTG-TEST-0283 — Incorrect Implementation of Server Hostname Verification: This test evaluates whether an Android app implements a `HostnameVerifier` that uses `verify(...)`) in an unsafe manner, effectively turning off hostname validation for the affected connections.
- MASTG-TEST-0284 — Incorrect SSL Error Handling in WebViews: This test evaluates whether an Android app has WebViews that ignore SSL/TLS certificate errors by overriding the `onReceivedSslError(...)` method without proper validation.
- MASTG-TEST-0285 — Outdated Android Version Allowing Trust in User-Provided CAs: This test evaluates whether an Android app **implicitly** trusts user-added CA certificates by default, which is the case for apps that can be installed to devices running API level 23 or lower.
- MASTG-TEST-0286 — Network Security Configuration Allowing Trust in User-Provided CAs: This test evaluates whether an Android app **explicitly** trusts user-added CA certificates by including `<certificates src="user"/>` in its Network Security Configuration which is defined `android:networkSecurityConfig` attribute is...
- MASTG-TEST-0396 — References to URLSessionDelegate Bypassing Certificate Validation: iOS apps that use `URLSession` can optionally override the system's default server trust evaluation by implementing `urlSession(_:didReceive:completionHandler:)` from `URLSessionDelegate` (session-level) or...
- MASTG-TEST-0397 — References to WKNavigationDelegate Bypassing Certificate Validation: `WKWebView` handles server authentication challenges through `WKNavigationDelegate.webView(_:didReceive:completionHandler:)`. When the app provides a navigation delegate that implements this method, the WebView's default certificate...

Mapped MASTG best practices:

- MASTG-BEST-0021 — Ensure Proper Error and Exception Handling: Secure exception and error handling in Android is about preventing the leakage of sensitive information, managing failures gracefully, and ensuring that errors do not compromise security. User-facing error messages should remain...
- MASTG-BEST-0073 — Properly Validate Server Trust in URLSessionDelegate and WKNavigationDelegate: When an iOS app overrides the default certificate validation by implementing `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)`) or `WKNavigationDelegate.webView(_:didReceive:completionHandler:)`), it takes full control of...

Mapped MASTG knowledge:

- MASTG-KNOW-0010 — Exception Handling: Exceptions occur when an application gets into an abnormal or error state. Both Java and C++ may throw exceptions. Testing exception handling is about ensuring that the app will handle an exception and transition to a safe state without...
- MASTG-KNOW-0014 — Android Network Security Configuration: Starting on Android 7.0 (API level 24), Android apps can customize their network security settings using the so-called Network Security Configuration feature which offers the following key capabilities:
- MASTG-KNOW-0072 — Server Trust Evaluation: ATS imposes extended security checks that supplement the default server trust evaluation prescribed by the Transport Layer Security (TLS) protocol. Loosening ATS restrictions reduces the security of the app. Apps should prefer...
