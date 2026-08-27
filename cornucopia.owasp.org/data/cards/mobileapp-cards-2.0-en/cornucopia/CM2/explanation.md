## Scenario: Garth can reduce app users' privacy because the app does not clearly disclose the sensitive data or tracking domains it accesses, collects, uses, or shares

### Example

Garth joins a supermarket loyalty scheme whose sign-up screen promises discounts while a tiny, forgotten settings page sends aisle visits to three advertising domains. The receipt later recommends “midnight snack routes,” although Garth only bought carrots.

People cannot make an informed privacy choice when collection and sharing are hidden. Clear notices must name sensitive data and tracking destinations; otherwise the app quietly turns ordinary shopping into an undeclared surveillance program.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure** in STRIDE. The named condition is: Garth can reduce app users' privacy because the app does not clearly disclose the sensitive data or tracking domains it accesses, collects, uses, or shares.

- **MAS-THREAT-0073:** Apps and embedded third-party components can collect or share more data than users were led to expect.
- **MAS-THREAT-0074:** Apps and embedded third-party components can track users against their expressed preferences.
- **MAS-THREAT-0066:** Apps and embedded third-party components can access more sensitive device resources and data than needed.

- **MAS-ATTACK-0081:** Collecting or sharing data categories that are not declared in the platform's privacy labels.
- **MAS-ATTACK-0082:** Transmitting undeclared identifiers or analytics data to first- or third-party services over the network.
- **MAS-ATTACK-0074:** Collecting and correlating identifiers and usage data across apps, devices, and services.
- **MAS-ATTACK-0075:** Contacting undeclared tracking domains that platform enforcement cannot block.
- **MAS-ATTACK-0088:** Holding excessive or no-longer-needed permissions granted to the app.
- **MAS-ATTACK-0089:** Using permissions granted to the host app to call protected APIs and collect data from a third-party SDK.

### What can go wrong?

If Garth can reduce app users' privacy because the app does not clearly disclose the sensitive data or tracking domains it accesses, collects, uses, or shares, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Collecting or sharing data categories that are not declared in the platform's privacy labels. Also, Transmitting undeclared identifiers or analytics data to first- or third-party services over the network. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0073 — Inadequate Data Collection Declarations: This weakness occurs when an app's stated data collection practices, such as those documented in Apple's App Privacy Report and Privacy Nutrition Labels, or Google's Data Safety section, are incomplete or inconsistent with the app's...
- MASWE-0074 — Inadequate Tracking Domains Declarations: This weakness occurs when an app fails to declare the domains it uses for tracking, declares them incompletely, or declares them inconsistently with its actual network behavior.
- MASWE-0066 — Inadequate Permission Management: This weakness occurs when an app requests more permissions than it needs, keeps permissions it no longer needs, or fails to explain why permissions are required.

### What are we going to do about it?

Inventory data categories, identifiers, SDKs, and tracking domains, disclose them in the platform privacy labels and consent UI, and send only the minimum necessary data; capture traffic and exercise SDK calls to verify declarations match behavior.


Mapped MASTG tests:

- MASTG-TEST-0206 — Undeclared PII in Network Traffic Capture: Attackers may capture network traffic from Android devices using an intercepting proxy, such as @MASTG-TOOL-0079, @MASTG-TOOL-0077, or @MASTG-TOOL-0097, to analyze the data being transmitted by the app. This works even if the app uses...
- MASTG-TEST-0281 — Undeclared Known Tracking Domains: This test identifies whether the app properly declares all known tracking domains it may communicate with in the `NSPrivacyTrackingDomains` section of its Privacy Manifest files.
- MASTG-TEST-0318 — References to SDK APIs Known to Handle Sensitive User Data: This test verifies whether an app uses SDK (third-party library) APIs known to handle sensitive user data (e.g., as defined in Google Play's Data safety section or the relevant privacy regulations).
- MASTG-TEST-0319 — Runtime Use of SDK APIs Known to Handle Sensitive User Data: This test is the dynamic counterpart to @MASTG-TEST-0318.
- MASTG-TEST-0360 — Purpose String Accuracy for Reachable Protected Resource Access: Purpose strings are user-facing explanations that iOS displays when an app requests access to protected resources such as location, camera, microphone, contacts, photos, health data, Bluetooth, motion, or speech recognition. Unlike...
- MASTG-TEST-0361 — Runtime Use of Protected Resource APIs Without Accurate Purpose Strings: This test is the dynamic counterpart to @MASTG-TEST-0360. See @MASTG-TEST-0360 for background on the relationship between protected resources, usage description keys, purpose strings, and framework APIs.

Mapped MASTG best practices:

- MASTG-BEST-0051 — Minimize iOS Permissions and Entitlements: Request only the iOS permissions and app capabilities that the app actually needs, and prefer the narrowest Apple-supported access model for each feature. This reduces unnecessary exposure of personal data and limits the blast radius if...

Mapped MASTG knowledge:

- MASTG-KNOW-0077 — App Permissions: iOS permissions work differently from Android. On Android, permissions are declared in a manifest and granted at install time or via runtime prompts. On iOS, access control is a layered model that is worth understanding before diving...
