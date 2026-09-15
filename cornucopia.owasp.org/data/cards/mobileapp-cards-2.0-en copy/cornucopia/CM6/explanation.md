## Scenario: Kim can reduce app users' privacy because the app repurpose biometric information (e.g. fingerprints, facial recognition data, etc.) collected for security concerns in order to cater for commercial interests

### Example

Kim unlocks a gym turnstile with facial recognition, then notices the gym’s snack kiosk advertising “your favorite protein bar” based on the same face template. The kiosk cannot explain why a security camera now thinks Kim needs chocolate-flavored recovery powder.

Biometric information gathered for access control must not be repurposed to sell products without permission. Treating a security measurement as a marketing asset exposes particularly sensitive data to a new commercial use.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure** in STRIDE. The named condition is: Kim can reduce app users' privacy because the app repurpose biometric information (e.g. fingerprints, facial recognition data, etc.) collected for security concerns in order to cater for commercial interests.

- **MAS-THREAT-0073:** Apps and embedded third-party components can collect or share more data than users were led to expect.
- **MAS-THREAT-0066:** Apps and embedded third-party components can access more sensitive device resources and data than needed.

- **MAS-ATTACK-0081:** Collecting or sharing data categories that are not declared in the platform's privacy labels.
- **MAS-ATTACK-0082:** Transmitting undeclared identifiers or analytics data to first- or third-party services over the network.
- **MAS-ATTACK-0088:** Holding excessive or no-longer-needed permissions granted to the app.
- **MAS-ATTACK-0089:** Using permissions granted to the host app to call protected APIs and collect data from a third-party SDK.

### What can go wrong?

If Kim can reduce app users' privacy because the app repurpose biometric information (e.g. fingerprints, facial recognition data, etc.) collected for security concerns in order to cater for commercial interests, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Collecting or sharing data categories that are not declared in the platform's privacy labels. Also, Transmitting undeclared identifiers or analytics data to first- or third-party services over the network. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0073 — Inadequate Data Collection Declarations: This weakness occurs when an app's stated data collection practices, such as those documented in Apple's App Privacy Report and Privacy Nutrition Labels, or Google's Data Safety section, are incomplete or inconsistent with the app's...
- MASWE-0066 — Inadequate Permission Management: This weakness occurs when an app requests more permissions than it needs, keeps permissions it no longer needs, or fails to explain why permissions are required.

### What are we going to do about it?

Use biometrics through the platform authentication API and keep raw biometric data out of app and analytics storage; obtain clear consent for any secondary use, minimize metadata, and test SDK calls and network traffic for biometric disclosure.


Mapped MASTG tests:

- MASTG-TEST-0206 — Undeclared PII in Network Traffic Capture: Attackers may capture network traffic from Android devices using an intercepting proxy, such as @MASTG-TOOL-0079, @MASTG-TOOL-0077, or @MASTG-TOOL-0097, to analyze the data being transmitted by the app. This works even if the app uses...
- MASTG-TEST-0318 — References to SDK APIs Known to Handle Sensitive User Data: This test verifies whether an app uses SDK (third-party library) APIs known to handle sensitive user data (e.g., as defined in Google Play's Data safety section or the relevant privacy regulations).
- MASTG-TEST-0319 — Runtime Use of SDK APIs Known to Handle Sensitive User Data: This test is the dynamic counterpart to @MASTG-TEST-0318.
- MASTG-TEST-0360 — Purpose String Accuracy for Reachable Protected Resource Access: Purpose strings are user-facing explanations that iOS displays when an app requests access to protected resources such as location, camera, microphone, contacts, photos, health data, Bluetooth, motion, or speech recognition. Unlike...
- MASTG-TEST-0361 — Runtime Use of Protected Resource APIs Without Accurate Purpose Strings: This test is the dynamic counterpart to @MASTG-TEST-0360. See @MASTG-TEST-0360 for background on the relationship between protected resources, usage description keys, purpose strings, and framework APIs.

Mapped MASTG best practices:

- MASTG-BEST-0051 — Minimize iOS Permissions and Entitlements: Request only the iOS permissions and app capabilities that the app actually needs, and prefer the narrowest Apple-supported access model for each feature. This reduces unnecessary exposure of personal data and limits the blast radius if...

Mapped MASTG knowledge:

- MASTG-KNOW-0077 — App Permissions: iOS permissions work differently from Android. On Android, permissions are declared in a manifest and granted at install time or via runtime prompts. On iOS, access control is a layered model that is worth understanding before diving...
