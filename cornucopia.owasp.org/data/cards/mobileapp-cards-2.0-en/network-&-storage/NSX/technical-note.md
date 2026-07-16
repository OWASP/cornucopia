## Platform-Aware Review Guidance

**Android**
- Lint rule: `TrustAllX509TrustManager` and `AllowAllHostnameVerifier` are flagged by Android Lint; enable in CI.
- Use `OkHttpClient.Builder().build()` without a custom `SSLSocketFactory`; the default uses the system trust store.
- `Network Security Config`: set `cleartextTrafficPermitted="false"` and do not include `<certificates src="user"/>` in release builds.
- Static analysis: grep for `TrustAllX509TrustManager`, `ALLOW_ALL_HOSTNAME_VERIFIER`, `setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER)`.

**iOS**
- `NSURLSessionDelegate.urlSession(_:didReceive:completionHandler:)`: call `.useCredential` only if the certificate chain is valid; call `.cancelAuthenticationChallenge` on failure.
- ATS enforcement: `NSAllowsArbitraryLoads = false`; document and justify any `NSExceptionDomains`.
- Static analysis: grep for `credential.trust` without certificate validation, `SecTrustEvaluate` called without checking the result.

**Testing**
- Use mitmproxy or Burp Suite with a custom CA; verify the app refuses connection.
- Test with an expired certificate; verify the app refuses connection.
- Test with a certificate for the wrong hostname; verify the app refuses connection.

**OWASP Mappings**
- MASVS: NETWORK-1
- MASTG: TEST-0019, TEST-0021, TEST-0023, TEST-0065, TEST-0067, TEST-0234, TEST-0282, TEST-0283, TEST-0284, TEST-0285, TEST-0286, TEST-0295, TEST-0396, TEST-0397
- MASWE: MASWE-0052
