## Scenario: Adrian can compromise the app communication through a proxy because the app does not use certificate pinning or implements it incorrectly

Consider a scenario where Adrian sets up Burp Suite as an intercepting proxy and installs the Burp CA certificate into the device's user certificate store. The app trusts all certificates in the device's user store. Adrian now intercepts, reads, and modifies every API call the app makes, including authentication requests containing credentials. There is no certificate pinning. The server's TLS certificate is valid. The connection is "secure" in the usual sense — just not from Adrian.

1. TLS without certificate pinning protects against passive interception by third parties, but not against an attacker who can install a trusted CA certificate.
2. Incorrect certificate pinning (pinning the wrong certificate, not checking the full chain, pinning only in debug builds) provides the appearance of pinning without the protection.
3. Public-key pinning with insufficient backup pins causes outages during certificate rotation.

### Example

Adrian installs a testing CA into the Android user trust store. For Android 7+, apps that do not opt in to trusting user certificates via a Network Security Config (`<certificates src="user" />`) will not trust his CA — but the app has not set `cleartextTrafficPermitted="false"` and does include `<certificates src="user" />` in the debug config that was accidentally shipped in the release build. Adrian intercepts the app's login request and reads the credentials in the proxy. The production release trusted his debug CA.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

Without certificate pinning, any party who can insert a trusted CA into the device's trust store (the device owner, an MDM, a malicious profile) can perform a man-in-the-middle attack, reading and modifying all TLS-protected communication.

### What can go wrong?

- Authentication credentials are captured and replayed.
- API responses are modified to grant additional access or inject malicious content.
- Sensitive PII transmitted over the network is intercepted.
- Debug Network Security Config settings shipped in release builds inadvertently trust user-installed CAs.

### What are we going to do about it?

- Implement certificate pinning using the server's public key or certificate hash; pin at least two pins (primary + backup) to avoid outage during rotation.
- Use `network_security_config.xml` on Android with `<pin-set>` configured for all pinned domains.
- On iOS, implement pinning in `URLSession` delegate `urlSession(_:didReceive:completionHandler:)` or use a library with a documented pinning implementation.
- Ensure the Network Security Config does not allow `user` certificate trust in release builds; review debug and release config separately.
