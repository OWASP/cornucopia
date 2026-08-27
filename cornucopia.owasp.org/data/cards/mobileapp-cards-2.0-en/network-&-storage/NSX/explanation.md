## Scenario: Adrian can compromise the app communication through a proxy because the app does not make use of certificate pinning or implements it incorrectly

### Example

Adrian’s shopping app trusts a proxy certificate installed by a “free faster Wi-Fi” profile. The proxy replaces a refund request with an order for 60 inflatable flamingos, which arrive with the confidence of a parade.

Certificate pinning can limit trusted intermediaries when the threat model requires it, but it must be implemented correctly and updated safely. Broken or absent pinning leaves the app’s traffic open to proxy interception.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Elevation of Privilege** in STRIDE. The named condition is: Adrian can compromise the app communication through a proxy because the app does not make use of certificate pinning or implements it incorrectly.

- **MAS-THREAT-0028:** Attackers can intercept or modify TLS-protected traffic even when standard certificate validation succeeds.

- **MAS-ATTACK-0014:** Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point.
- **MAS-ATTACK-0016:** Obtaining a valid certificate for the target domain from a compromised, coerced, or rogue Certificate Authority (CA).
- **MAS-ATTACK-0017:** Installing an attacker-controlled CA certificate on a device they control to inspect the app's traffic.

### What can go wrong?

If Adrian can compromise the app communication through a proxy because the app does not make use of certificate pinning or implements it incorrectly, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point. Also, Obtaining a valid certificate for the target domain from a compromised, coerced, or rogue Certificate Authority (CA). That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0062 — No Application-Level Payload Encryption: This weakness occurs when an app relies solely on transport-layer encryption for its network traffic, without an additional layer of application-level payload encryption.
- MASWE-0028 — Insecure Identity Pinning: This weakness occurs when identity pinning (also known as certificate pinning, public key pinning, or TLS pinning) is not implemented, or is implemented incorrectly, so the app cannot guarantee that it only communicates with servers...

### What are we going to do about it?

Implement certificate or public-key pinning only with a documented rotation and recovery plan, keep normal chain validation enabled, and test an intercepting proxy, expired pins, and update transitions so bypasses fail safely.


Mapped MASTG tests:

- MASTG-TEST-0242 — Missing Certificate Pinning in Network Security Configuration: Apps can configure certificate pinning using the Network Security Configuration. For each domain, one or multiple digests can be pinned.
- MASTG-TEST-0243 — Expired Certificate Pins in the Network Security Configuration: Apps can configure expiration dates for pinned certificates in the Network Security Configuration (NSC) (@MASTG-KNOW-0014) by using the `expiration` attribute. When a pin expires, the app no longer enforces certificate pinning and...
- MASTG-TEST-0244 — Missing Certificate Pinning in Network Traffic: There are multiple ways an application can implement certificate pinning, including via the Android Network Security Config, custom TrustManager implementations, third-party libraries, and native code. Since some implementations might...
- MASTG-TEST-0385 — Missing Certificate Pinning in ATS: iOS apps can configure certificate pinning via App Transport Security (ATS) by declaring expected CA or leaf certificate public key hashes in the `Info.plist` file under the `NSPinnedDomains` key. This is Apple's built-in mechanism for...

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0014 — Android Network Security Configuration: Starting on Android 7.0 (API level 24), Android apps can customize their network security settings using the so-called Network Security Configuration feature which offers the following key capabilities:
- MASTG-KNOW-0015 — Certificate Pinning: Certificate pinning can be employed in Android apps to safeguard against Machine-in-the-Middle (MITM) attacks by ensuring that the app communicates exclusively with remote endpoints possessing specific identities.
- MASTG-KNOW-0072 — Server Trust Evaluation: ATS imposes extended security checks that supplement the default server trust evaluation prescribed by the Transport Layer Security (TLS) protocol. Loosening ATS restrictions reduces the security of the app. Apps should prefer...
