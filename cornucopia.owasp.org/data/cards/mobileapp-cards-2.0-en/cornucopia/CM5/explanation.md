## Scenario: Debarghaya can reduce app users' privacy because the app repurposes personal data collected for security or fraud prevention for commercial purposes without informed consent

### Example

Debarghaya installs a banking app that asks for device signals to spot fraud. A month later, the same “security” scores are sold to a retailer that labels him a premium customer and offers a gold-plated toaster at a suspiciously precise price.

Information collected to protect an account cannot silently become a marketing profile. Repurposing fraud data for commerce without informed consent changes the bargain users accepted and erodes their privacy.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure** in STRIDE. The named condition is: Debarghaya can reduce app users' privacy because the app repurposes personal data collected for security or fraud prevention for commercial purposes without informed consent.

- **MAS-THREAT-0073:** Apps and embedded third-party components can collect or share more data than users were led to expect.

- **MAS-ATTACK-0081:** Collecting or sharing data categories that are not declared in the platform's privacy labels.
- **MAS-ATTACK-0082:** Transmitting undeclared identifiers or analytics data to first- or third-party services over the network.

### What can go wrong?

If Debarghaya can reduce app users' privacy because the app repurposes personal data collected for security or fraud prevention for commercial purposes without informed consent, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Collecting or sharing data categories that are not declared in the platform's privacy labels. Also, Transmitting undeclared identifiers or analytics data to first- or third-party services over the network. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0073 — Inadequate Data Collection Declarations: This weakness occurs when an app's stated data collection practices, such as those documented in Apple's App Privacy Report and Privacy Nutrition Labels, or Google's Data Safety section, are incomplete or inconsistent with the app's...

### What are we going to do about it?

Keep fraud and security data limited to that purpose and retention period, obtain separate informed consent for any commercial use, and prevent analytics or advertising SDKs from receiving it; test SDK APIs and runtime network traffic for repurposing.


Mapped MASTG tests:

- MASTG-TEST-0318 — References to SDK APIs Known to Handle Sensitive User Data: This test verifies whether an app uses SDK (third-party library) APIs known to handle sensitive user data (e.g., as defined in Google Play's Data safety section or the relevant privacy regulations).
- MASTG-TEST-0319 — Runtime Use of SDK APIs Known to Handle Sensitive User Data: This test is the dynamic counterpart to @MASTG-TEST-0318.

Mapped MASTG best practices:

- No MASTG best practice is assigned; use the narrowest platform control that blocks the attack.

Mapped MASTG knowledge:

- MASTG-KNOW-0026 — Third-party Services Embedded in the App: The features provided by third-party services can involve tracking services to monitor the user's behavior while using the app, selling banner advertisements, or improving the user experience.
