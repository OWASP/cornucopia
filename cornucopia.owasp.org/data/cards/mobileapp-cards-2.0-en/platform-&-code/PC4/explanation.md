## Scenario: Kelly can expose sensitive data by taking advantage of excessive, unexplained, or unjustified permissions and entitlements for location, camera, microphone, storage, health data, etc

### Example

Kelly installs a flashlight app that requests location, microphone, contacts, camera, health data, and storage. The flashlight never turns on, but an advertising dashboard confidently reports that Kelly is standing near a yoga studio.

Permissions and entitlements should be limited to a documented need and explained to the user. Excessive access gives the app or its components opportunities to expose information unrelated to the feature.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Kelly can expose sensitive data by taking advantage of excessive, unexplained, or unjustified permissions and entitlements for location, camera, microphone, storage, health data, etc.

- **MAS-THREAT-0066:** Apps and embedded third-party components can access more sensitive device resources and data than needed.

- **MAS-ATTACK-0088:** Holding excessive or no-longer-needed permissions granted to the app.
- **MAS-ATTACK-0089:** Using permissions granted to the host app to call protected APIs and collect data from a third-party SDK.

### What can go wrong?

If Kelly can expose sensitive data by taking advantage of excessive, unexplained, or unjustified permissions and entitlements for location, camera, microphone, storage, health data, etc, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Holding excessive or no-longer-needed permissions granted to the app. Also, Using permissions granted to the host app to call protected APIs and collect data from a third-party SDK. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0066 — Inadequate Permission Management: This weakness occurs when an app requests more permissions than it needs, keeps permissions it no longer needs, or fails to explain why permissions are required.

### What are we going to do about it?

Request only the runtime permissions and entitlements the feature needs, explain them at the point of use, revoke or stop using them when no longer needed, and test denied, revoked, background, and overbroad-permission cases.


Mapped MASTG tests:

- MASTG-TEST-0254 — Dangerous App Permissions: In Android apps, permissions are acquired through different methods to access information and system functionalities, including the camera, location, or storage. The necessary permissions are specified in the `AndroidManifest.xml` file...
- MASTG-TEST-0255 — Permission Requests Not Minimized: The source provides the mapped security guidance for this control.
- MASTG-TEST-0256 — Missing Permission Rationale: The source provides the mapped security guidance for this control.
- MASTG-TEST-0257 — Not Resetting Unused Permissions: The source provides the mapped security guidance for this control.
- MASTG-TEST-0360 — Purpose String Accuracy for Reachable Protected Resource Access: Purpose strings are user-facing explanations that iOS displays when an app requests access to protected resources such as location, camera, microphone, contacts, photos, health data, Bluetooth, motion, or speech recognition. Unlike...
- MASTG-TEST-0361 — Runtime Use of Protected Resource APIs Without Accurate Purpose Strings: This test is the dynamic counterpart to @MASTG-TEST-0360. See @MASTG-TEST-0360 for background on the relationship between protected resources, usage description keys, purpose strings, and framework APIs.
- MASTG-TEST-0362 — Entitlements for Unjustified Capability Exposure: Entitlements are signed rights or privileges that enable an iOS app or app extension to use specific platform services, capabilities, or system integrations. Unlike purpose strings, entitlements are not limited to protected resources or...
- MASTG-TEST-0363 — Runtime Use of Entitlement-Backed APIs for Unjustified Capability Exposure: This test is the dynamic counterpart to @MASTG-TEST-0362. See @MASTG-TEST-0362 for background on the relationship between Xcode capabilities, signed entitlements, and entitlement-backed APIs or entry points.

Mapped MASTG best practices:

- MASTG-BEST-0051 — Minimize iOS Permissions and Entitlements: Request only the iOS permissions and app capabilities that the app actually needs, and prefer the narrowest Apple-supported access model for each feature. This reduces unnecessary exposure of personal data and limits the blast radius if...

Mapped MASTG knowledge:

- MASTG-KNOW-0017 — App Permissions: Android assigns a distinct system identity (Linux user ID and group ID) to every installed app. Because each Android app operates in a process sandbox, apps must explicitly request access to resources and data that are outside their...
- MASTG-KNOW-0077 — App Permissions: iOS permissions work differently from Android. On Android, permissions are declared in a manifest and granted at install time or via runtime prompts. On iOS, access control is a layered model that is worth understanding before diving...
