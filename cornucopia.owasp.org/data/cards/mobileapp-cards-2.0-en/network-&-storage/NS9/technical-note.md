## Technical Note: Adrian can compromise the app communication through a proxy because the app does not make use of certificate pinning or implements it incorrectly

### Platform Guidance

**Android:** Implement certificate pinning carefully and rotate pins with backups so the app is resistant to hostile proxies without becoming a self-inflicted outage machine.

```kotlin
val pinner = CertificatePinner.Builder()
.add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
.build()
```

**iOS:** Use `URLSessionDelegate` trust evaluation or a vetted library to compare the server certificate or SPKI against an allowlist.

```swift
func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge, completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
guard PinningEvaluator.trusts(challenge.protectionSpace.serverTrust) else {
    return completionHandler(.cancelAuthenticationChallenge, nil)
}
completionHandler(.useCredential, URLCredential(trust: challenge.protectionSpace.serverTrust!))
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0022, MASTG-TEST-0068
**New Tests:** MASTG-TEST-0217, MASTG-TEST-0235, MASTG-TEST-0239, MASTG-TEST-0282, MASTG-TEST-0286, MASTG-TEST-0323, MASTG-TEST-0345, MASTG-TEST-0397

### MASWE Weaknesses

- MASWE-0047, MASWE-0051: pinning and trust-anchor handling weaknesses that enable proxy-based interception.
