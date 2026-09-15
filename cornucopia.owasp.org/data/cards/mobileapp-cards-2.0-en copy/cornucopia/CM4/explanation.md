## Scenario: Elizabeth can reduce app users' privacy because the app does not clearly disclose, or obtain the user's consent for, personal data it shares with downstream services.

### Example

Elizabeth orders flowers through an app that shares her address with a delivery subcontractor. The checkout mentions “partners” once, and the subcontractor then sends her a birthday bouquet addressed to the entire office because nobody explained what was being shared.

Downstream services need disclosed data flows and meaningful consent. Hiding the recipient and purpose prevents Elizabeth from deciding whether that personal information may leave the app, even if the transfer is operationally convenient.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Denial of Service** in STRIDE. The named condition is: Elizabeth can reduce app users' privacy because the app does not clearly disclose, or obtain the user's consent for, personal data it shares with downstream services..

- **MAS-THREAT-0073:** Apps and embedded third-party components can collect or share more data than users were led to expect.
- **MAS-THREAT-0074:** Apps and embedded third-party components can track users against their expressed preferences.

- **MAS-ATTACK-0081:** Collecting or sharing data categories that are not declared in the platform's privacy labels.
- **MAS-ATTACK-0082:** Transmitting undeclared identifiers or analytics data to first- or third-party services over the network.
- **MAS-ATTACK-0074:** Collecting and correlating identifiers and usage data across apps, devices, and services.
- **MAS-ATTACK-0075:** Contacting undeclared tracking domains that platform enforcement cannot block.

### What can go wrong?

If Elizabeth can reduce app users' privacy because the app does not clearly disclose, or obtain the user's consent for, personal data it shares with downstream services., the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Collecting or sharing data categories that are not declared in the platform's privacy labels. Also, Transmitting undeclared identifiers or analytics data to first- or third-party services over the network. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0073 — Inadequate Data Collection Declarations: This weakness occurs when an app's stated data collection practices, such as those documented in Apple's App Privacy Report and Privacy Nutrition Labels, or Google's Data Safety section, are incomplete or inconsistent with the app's...
- MASWE-0074 — Inadequate Tracking Domains Declarations: This weakness occurs when an app fails to declare the domains it uses for tracking, declares them incompletely, or declares them inconsistently with its actual network behavior.

### What are we going to do about it?

Tell users which downstream services receive personal data, obtain specific consent before sharing, minimize each payload, and enforce the same limits in SDK configuration; verify network captures and third-party calls against the declared purposes.


Mapped MASTG tests:

- MASTG-TEST-0206 — Undeclared PII in Network Traffic Capture: Attackers may capture network traffic from Android devices using an intercepting proxy, such as @MASTG-TOOL-0079, @MASTG-TOOL-0077, or @MASTG-TOOL-0097, to analyze the data being transmitted by the app. This works even if the app uses...
- MASTG-TEST-0281 — Undeclared Known Tracking Domains: This test identifies whether the app properly declares all known tracking domains it may communicate with in the `NSPrivacyTrackingDomains` section of its Privacy Manifest files.
- MASTG-TEST-0318 — References to SDK APIs Known to Handle Sensitive User Data: This test verifies whether an app uses SDK (third-party library) APIs known to handle sensitive user data (e.g., as defined in Google Play's Data safety section or the relevant privacy regulations).
- MASTG-TEST-0319 — Runtime Use of SDK APIs Known to Handle Sensitive User Data: This test is the dynamic counterpart to @MASTG-TEST-0318.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- No MASTG knowledge entry is assigned; document the platform behavior discovered during review.
