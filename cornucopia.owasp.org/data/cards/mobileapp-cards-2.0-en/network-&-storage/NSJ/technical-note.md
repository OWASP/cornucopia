## Technical Note: Nihel can compromise the communication as it may fall back to an insecure or unencrypted channel,  because encryption is optional, or because of client-server protocol or security provider weaknesses

### Platform Guidance

**Android:** Disable cleartext fallback and protocol downgrade paths so the network stack cannot casually wander into the 1990s.

```kotlin
<application
android:usesCleartextTraffic="false"
android:networkSecurityConfig="@xml/network_security_config" />
```

**iOS:** Enforce ATS and reject alternate unencrypted endpoints or retry logic that quietly swaps to HTTP.

```swift
<key>NSAppTransportSecurity</key>
<dict>
<key>NSAllowsArbitraryLoads</key><false/>
</dict>
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0020, MASTG-TEST-0023, MASTG-TEST-0066
**New Tests:** MASTG-TEST-0233, MASTG-TEST-0237, MASTG-TEST-0243, MASTG-TEST-0284, MASTG-TEST-0321, MASTG-TEST-0343, MASTG-TEST-0385

### MASWE Weaknesses

- MASWE-0049: downgrade and insecure-fallback behavior in transport security.
