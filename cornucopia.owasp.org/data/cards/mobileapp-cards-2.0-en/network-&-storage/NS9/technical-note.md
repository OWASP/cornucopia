## Platform-Aware Review Guidance

**Android**
- `network_security_config.xml`:
  ```xml
  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.example.com</domain>
    <pin-set expiration="2026-01-01">
      <pin digest="SHA-256">primaryHash=</pin>
      <pin digest="SHA-256">backupHash=</pin>
    </pin-set>
  </domain-config>
  ```
- Verify the release build references the production config, not the debug config.
- OkHttp: use `CertificatePinner` to add per-domain pins programmatically.

**iOS**
- Implement `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)` and validate the server certificate against stored public-key hashes.
- TrustKit: a popular iOS/macOS library for certificate pinning with backup-pin support.
- App Transport Security (ATS): ensure `NSAllowsArbitraryLoads` is `false` in production builds.

**Rotation Planning**
- Always pin at least two keys: the current leaf/CA and a backup (the next CA or a pre-generated backup key).
- Set a certificate expiry date in the pin-set and use a push-update mechanism to rotate pins before expiry.

**Testing**
- Install Burp Suite CA in the user store and verify the app rejects the connection (Android 7+ default, or with pinning).
- Test on Android with a custom user CA; verify `SSLPeerUnverifiedException` is thrown and the connection is rejected.
- Verify the app handles pin validation failure gracefully (error message, no crash, no fallback to unpinned connection).

**OWASP Mappings**
- MASVS: NETWORK-2
- MASTG: TEST-0022, TEST-0068, TEST-0242, TEST-0243, TEST-0244, TEST-0385
- MASWE: MASWE-0047
