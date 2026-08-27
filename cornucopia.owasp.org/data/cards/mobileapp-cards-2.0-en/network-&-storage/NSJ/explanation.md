## Scenario: Nihel can expose or modify data in transit because the app permits cleartext traffic or allows downgrade to deprecated TLS protocol versions

### Example

Nihel checks a weather app at a ferry terminal where the server accepts cleartext and negotiates an obsolete TLS version. A nearby observer changes “rain tomorrow” to “free ice cream,” sending Nihel onto the pier with a cone-shaped optimism.

Cleartext and deprecated TLS leave the connection open to eavesdropping and alteration. The app should require current authenticated transport instead of letting a network intermediary turn a forecast into an expensive dessert expedition.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Nihel can expose or modify data in transit because the app permits cleartext traffic or allows downgrade to deprecated TLS protocol versions.

- **MAS-THREAT-0026:** Attackers can intercept or modify cleartext network traffic.
- **MAS-THREAT-0027:** Attackers can intercept or modify TLS-protected network traffic.

- **MAS-ATTACK-0012:** Monitoring network traffic on the same network (e.g., public Wi-Fi or a compromised router).
- **MAS-ATTACK-0013:** Monitoring local or proximity interfaces such as Bluetooth, NFC, or USB.
- **MAS-ATTACK-0014:** Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point.
- **MAS-ATTACK-0015:** Presenting a fraudulent or otherwise invalid certificate that the app accepts.

### What can go wrong?

If Nihel can expose or modify data in transit because the app permits cleartext traffic or allows downgrade to deprecated TLS protocol versions, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Monitoring network traffic on the same network (e.g., public Wi-Fi or a compromised router). Also, Monitoring local or proximity interfaces such as Bluetooth, NFC, or USB. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0026 — Network Traffic Not Encrypted: This weakness occurs when an app transmits data over the network in cleartext, i.e. without encryption, making it accessible to anyone able to monitor the network channel.
- MASWE-0027 — Insecure Certificate Validation: This weakness occurs when an app does not properly validate TLS certificates during secure communication, accepting invalid, expired, self-signed, or untrusted certificates without appropriate verification.

### What are we going to do about it?

Disable cleartext traffic and deprecated TLS versions in Android Network Security Config or iOS ATS, require modern TLS with hostname and certificate validation, and test downgrade, plaintext, redirect, and failed-handshake paths.


Mapped MASTG tests:

- MASTG-TEST-0217 — Insecure TLS Protocols Explicitly Allowed in Code: The Android Network Security Configuration does not provide direct control over specific TLS versions (unlike iOS), and starting with Android 10, TLS v1.3 is enabled by default for all TLS connections.
- MASTG-TEST-0218 — Insecure TLS Protocols in Network Traffic: While static analysis can identify configurations that allow insecure TLS versions, it may not accurately reflect the actual protocol used during live communications. This is because TLS version negotiation occurs between the client...
- MASTG-TEST-0233 — Hardcoded HTTP URLs: An Android app may have hardcoded HTTP URLs embedded in the app binary, library binaries, or other resources within the APK. These URLs may indicate potential locations where the app communicates with servers over an unencrypted connection.
- MASTG-TEST-0235 — Android App Configurations Allowing Cleartext Traffic: Since Android 9 (API level 28) cleartext HTTP traffic is blocked by default (thanks to the default Network Security Configuration) but there are multiple ways in which an application can still send it:
- MASTG-TEST-0236 — Cleartext Traffic Observed on the Network: This test intercepts the app's incoming and outgoing network traffic, and checks for any cleartext communication.
- MASTG-TEST-0295 — GMS Security Provider Not Updated: This test checks whether the Android app ensures the Security Provider is updated to mitigate SSL/TLS vulnerabilities. The provider should be updated using Google Play Services APIs, and the implementation should handle exceptions properly.
- MASTG-TEST-0321 — Hardcoded HTTP URLs: An iOS app may have hardcoded HTTP URLs embedded in the app binary, library binaries, or other resources within the IPA. These URLs may indicate potential locations where the app communicates with servers over an unencrypted connection.
- MASTG-TEST-0322 — App Transport Security Configurations Allowing Cleartext Traffic: Since iOS 9 App Transport Security (ATS) blocks cleartext HTTP traffic by default for connections using the URL Loading System (typically via `URLSession`). However, an app can still send cleartext traffic through several ATS exceptions...
- MASTG-TEST-0323 — Uses of Low-Level Networking APIs for Cleartext Traffic: App Transport Security (ATS) only applies to connections made via the URL Loading System (typically `URLSession`). Lower-level networking APIs bypass ATS entirely, meaning they can establish cleartext HTTP connections regardless of the...
- MASTG-TEST-0342 — References to Weak ATS TLS Policy Exceptions in Info.plist: Apps can weaken ATS TLS enforcement through `NSAppTransportSecurity` exceptions in `Info.plist`. In particular:
- MASTG-TEST-0343 — URLSession TLS Protocol Configuration: `URLSessionConfiguration` allows apps to customize TLS behavior for individual `URLSession` instances. The `tlsMinimumSupportedProtocolVersion` property (or the deprecated `tlsMinimumSupportedProtocol`) controls the minimum TLS version...
- MASTG-TEST-0344 — Network.framework TLS Protocol Configuration: The Network framework operates entirely outside of ATS. Apps using `NWConnection` with `NWProtocolTLS.Options` can configure TLS settings directly via the Security framework, including minimum and maximum supported TLS versions through...
- MASTG-TEST-0345 — Embedded or Third-party TLS Stack Configuration: Some apps embed networking stacks that manage TLS independently from Apple's ATS-enforced URL Loading System. Examples include OpenSSL, BoringSSL, mbedTLS, curl, and gRPC. Since ATS doesn't apply to these libraries, any weak TLS...
- MASTG-TEST-0348 — Insecure TLS Protocols in Network Traffic: While static analysis can identify configurations that allow insecure TLS versions, it may not accurately reflect the actual protocol used during live communications. This is because TLS version negotiation occurs between the client...

Mapped MASTG best practices:

- MASTG-BEST-0020 — Update the GMS Security Provider: Android devices vary widely in OS version and update frequency. Relying solely on platform-level security can leave apps exposed to outdated SSL/TLS implementations and known vulnerabilities.
- MASTG-BEST-0042 — Use Strong TLS Settings in ATS Configuration: App Transport Security (ATS) enforces strong TLS defaults for `URLSession` connections on iOS 9 and later. Avoid weakening these defaults through ATS exceptions in `Info.plist`, and ensure any custom TLS configuration in code is equally...
- MASTG-BEST-0043 — Enforce Strong TLS Settings When ATS Doesn't Apply: App Transport Security (ATS) only protects connections made through the URL Loading System (`URLSession` and related Foundation APIs). When your app uses Network.framework, CFNetwork, BSD sockets, or a bundled third-party TLS library,...

Mapped MASTG knowledge:

- MASTG-KNOW-0014 — Android Network Security Configuration: Starting on Android 7.0 (API level 24), Android apps can customize their network security settings using the so-called Network Security Configuration feature which offers the following key capabilities:
- MASTG-KNOW-0011 — Security Provider: Android relies on a security provider via the `java.security.Provider` class to implement Java Security services and provide SSL/TLS-based connections. These providers are crucial to ensure secure network communications and secure other...
- MASTG-KNOW-0010 — Exception Handling: Exceptions occur when an application gets into an abnormal or error state. Both Java and C++ may throw exceptions. Testing exception handling is about ensuring that the app will handle an exception and transition to a safe state without...
- MASTG-KNOW-0071 — iOS App Transport Security: Starting with iOS 9, Apple introduced App Transport Security (ATS) which is a set of security checks enforced by the operating system for connections made using the URL Loading System (typically via `URLSession`) to always use HTTPS....
- MASTG-KNOW-0073 — iOS Network APIs: On iOS, you can create network connections through multiple API layers. These layers differ in abstraction level, supported protocols, and how much of the connection lifecycle they manage. See "TN3151: Choosing the right networking API"...
