## Technical Note: Maarten can compromise the communication between the app and the external services because the app does not verify TLS certificates and -chains, trust insecure sources, lack hostname verification or ignore TLS verification issues

### Platform Guidance

**Android:** Validate the full certificate chain and hostname and refuse user-added trust shortcuts unless the business case is explicit and documented.

```kotlin
val client = OkHttpClient.Builder()
.hostnameVerifier { host, session -> HttpsURLConnection.getDefaultHostnameVerifier().verify(host, session) }
.build()
```

**iOS:** Use the system trust store correctly and reject invalid chains, mismatched hosts, or ad-hoc “accept anyway” paths.

```swift
guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
  let trust = challenge.protectionSpace.serverTrust,
  SecTrustEvaluateWithError(trust, nil) else {
completionHandler(.cancelAuthenticationChallenge, nil)
return
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0019, MASTG-TEST-0021, MASTG-TEST-0065, MASTG-TEST-0067
**New Tests:** MASTG-TEST-0218, MASTG-TEST-0236, MASTG-TEST-0242, MASTG-TEST-0283, MASTG-TEST-0295, MASTG-TEST-0342, MASTG-TEST-0348

### MASWE Weaknesses

- MASWE-0048, MASWE-0052: TLS validation, hostname verification, and trust-chain handling failures.
