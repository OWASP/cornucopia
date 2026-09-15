## Scenario: Ahmed can read and modify data in transit because the communication is transmitted over an unencrypted channel

### Example

Ahmed uses a parking app in an underground garage that sends his plate number and payment details over an unencrypted hotspot. A person beside the pay station changes the meter duration, and Ahmed returns to find a ticket for parking “until the next century.”

Sensitive communication needs an encrypted, authenticated channel rather than plain network transport. Anyone able to observe the connection can otherwise read and modify the data in transit.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Ahmed can read and modify data in transit because the communication is transmitted over an unencrypted channel.

- **MAS-THREAT-0026:** Attackers can intercept or modify cleartext network traffic.

- **MAS-ATTACK-0012:** Monitoring network traffic on the same network (e.g., public Wi-Fi or a compromised router).
- **MAS-ATTACK-0013:** Monitoring local or proximity interfaces such as Bluetooth, NFC, or USB.
- **MAS-ATTACK-0014:** Performing a Machine-in-the-Middle (MITM) attack, e.g., via ARP poisoning, DNS spoofing, or a rogue access point.

### What can go wrong?

If Ahmed can read and modify data in transit because the communication is transmitted over an unencrypted channel, the failure is concrete rather than merely theatrical: the app could let an attacker cross the network-&-storage boundary and reach data or capability that this flow should protect. In this card, the practical route includes Monitoring network traffic on the same network (e.g., public Wi-Fi or a compromised router). Also, Monitoring local or proximity interfaces such as Bluetooth, NFC, or USB. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0026 — Network Traffic Not Encrypted: This weakness occurs when an app transmits data over the network in cleartext, i.e. without encryption, making it accessible to anyone able to monitor the network channel.
- MASWE-0027 — Insecure Certificate Validation: This weakness occurs when an app does not properly validate TLS certificates during secure communication, accepting invalid, expired, self-signed, or untrusted certificates without appropriate verification.

### What are we going to do about it?

Route all sensitive communication through modern TLS with certificate and hostname validation, never silently fall back to HTTP or an unencrypted channel, and test traffic capture, downgrade, redirects, and malformed responses.


Mapped MASTG tests:

- MASTG-TEST-0321 — Hardcoded HTTP URLs: An iOS app may have hardcoded HTTP URLs embedded in the app binary, library binaries, or other resources within the IPA. These URLs may indicate potential locations where the app communicates with servers over an unencrypted connection.
- MASTG-TEST-0322 — App Transport Security Configurations Allowing Cleartext Traffic: Since iOS 9 App Transport Security (ATS) blocks cleartext HTTP traffic by default for connections using the URL Loading System (typically via `URLSession`). However, an app can still send cleartext traffic through several ATS exceptions...
- MASTG-TEST-0233 — Hardcoded HTTP URLs: An Android app may have hardcoded HTTP URLs embedded in the app binary, library binaries, or other resources within the APK. These URLs may indicate potential locations where the app communicates with servers over an unencrypted connection.
- MASTG-TEST-0235 — Android App Configurations Allowing Cleartext Traffic: Since Android 9 (API level 28) cleartext HTTP traffic is blocked by default (thanks to the default Network Security Configuration) but there are multiple ways in which an application can still send it:
- MASTG-TEST-0236 — Cleartext Traffic Observed on the Network: This test intercepts the app's incoming and outgoing network traffic, and checks for any cleartext communication.
- MASTG-TEST-0237 — Cross-Platform Framework Configurations Allowing Cleartext Traffic: The source provides the mapped security guidance for this control.
- MASTG-TEST-0238 — Runtime Use of Network APIs Transmitting Cleartext Traffic: The source provides the mapped security guidance for this control.
- MASTG-TEST-0239 — Using low-level APIs (e.g. Socket) to set up a custom HTTP connection: The source provides the mapped security guidance for this control.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0071 — iOS App Transport Security: Starting with iOS 9, Apple introduced App Transport Security (ATS) which is a set of security checks enforced by the operating system for connections made using the URL Loading System (typically via `URLSession`) to always use HTTPS....
- MASTG-KNOW-0014 — Android Network Security Configuration: Starting on Android 7.0 (API level 24), Android apps can customize their network security settings using the so-called Network Security Configuration feature which offers the following key capabilities:
