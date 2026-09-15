## Scenario: Mallory can use the app installed on Bob's device maliciously to surveil, spy on, eavesdrop, control remotely, track or otherwise monitor Bob, without consent and/or notification

### Example

Mallory borrows Bob’s phone during a family road trip and enables a navigation plug-in that records the cabin microphone and location. It later announces, “Bob is approaching the secret picnic,” ruining both the surprise and the sandwiches.

Permissions, component boundaries, and privacy signals should prevent covert surveillance or remote control. An app installed on Bob’s device must not let Mallory collect or use his sensitive resources without consent and notification.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure** in STRIDE. The named condition is: Mallory can use the app installed on Bob's device maliciously to surveil, spy on, eavesdrop, control remotely, track or otherwise monitor Bob, without consent and/or notification. This is a wildcard application attack: the story is an invented exercise, while the mapped control is still tested against the stated privacy impact.

- **MAS-THREAT-0073:** Apps and embedded third-party components can collect or share more data than users were led to expect.
- **MAS-THREAT-0066:** Apps and embedded third-party components can access more sensitive device resources and data than needed.
- **MAS-THREAT-0074:** Apps and embedded third-party components can track users against their expressed preferences.
- **MAS-THREAT-0018:** Attackers can access sensitive data and functionality exposed by app components.
- **MAS-THREAT-0032:** Attackers can intercept or manipulate the app's intents.

- **MAS-ATTACK-0081:** Collecting or sharing data categories that are not declared in the platform's privacy labels.
- **MAS-ATTACK-0082:** Transmitting undeclared identifiers or analytics data to first- or third-party services over the network.
- **MAS-ATTACK-0088:** Holding excessive or no-longer-needed permissions granted to the app.
- **MAS-ATTACK-0089:** Using permissions granted to the host app to call protected APIs and collect data from a third-party SDK.
- **MAS-ATTACK-0074:** Collecting and correlating identifiers and usage data across apps, devices, and services.
- **MAS-ATTACK-0075:** Contacting undeclared tracking domains that platform enforcement cannot block.
- **MAS-ATTACK-0038:** Invoking exported or unprotected app components from another app installed on the device.
- **MAS-ATTACK-0039:** Connecting to open ports or local services exposed by the app.
- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0049:** Registering intent filters to intercept implicit intents sent by the app.
- **MAS-ATTACK-0050:** Modifying or replaying mutable PendingIntents obtained from the app.

### What can go wrong?

If Mallory can use the app installed on Bob's device maliciously to surveil, spy on, eavesdrop, control remotely, track or otherwise monitor Bob, without consent and/or notification, the failure is concrete rather than merely theatrical: the app could let an attacker cross the wild-card boundary and reach data or capability that this flow should protect. In this card, the practical route includes Collecting or sharing data categories that are not declared in the platform's privacy labels. Also, Transmitting undeclared identifiers or analytics data to first- or third-party services over the network. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0073 — Inadequate Data Collection Declarations: This weakness occurs when an app's stated data collection practices, such as those documented in Apple's App Privacy Report and Privacy Nutrition Labels, or Google's Data Safety section, are incomplete or inconsistent with the app's...
- MASWE-0066 — Inadequate Permission Management: This weakness occurs when an app requests more permissions than it needs, keeps permissions it no longer needs, or fails to explain why permissions are required.
- MASWE-0074 — Inadequate Tracking Domains Declarations: This weakness occurs when an app fails to declare the domains it uses for tracking, declares them incompletely, or declares them inconsistently with its actual network behavior.
- MASWE-0018 — Lack of Authentication or Authorization on App Components: This weakness occurs when app components that expose functionality or data do not enforce proper authentication or authorization on their callers.
- MASWE-0032 — Insecure Intents: This weakness occurs when an app creates or handles Android intents insecurely, allowing other apps to intercept, redirect, or manipulate its communication.

### What are we going to do about it?

Request only necessary sensors, location, microphone, and accessibility capabilities, obtain visible informed consent, show clear recording or tracking indicators, and provide immediate stop and deletion controls; test background use and revocation on both platforms.


Mapped MASTG tests:

- MASTG-TEST-0206 — Undeclared PII in Network Traffic Capture: Attackers may capture network traffic from Android devices using an intercepting proxy, such as @MASTG-TOOL-0079, @MASTG-TOOL-0077, or @MASTG-TOOL-0097, to analyze the data being transmitted by the app. This works even if the app uses...
- MASTG-TEST-0254 — Dangerous App Permissions: In Android apps, permissions are acquired through different methods to access information and system functionalities, including the camera, location, or storage. The necessary permissions are specified in the `AndroidManifest.xml` file...
- MASTG-TEST-0255 — Permission Requests Not Minimized: The source provides the mapped security guidance for this control.
- MASTG-TEST-0256 — Missing Permission Rationale: The source provides the mapped security guidance for this control.
- MASTG-TEST-0281 — Undeclared Known Tracking Domains: This test identifies whether the app properly declares all known tracking domains it may communicate with in the `NSPrivacyTrackingDomains` section of its Privacy Manifest files.
- MASTG-TEST-0318 — References to SDK APIs Known to Handle Sensitive User Data: This test verifies whether an app uses SDK (third-party library) APIs known to handle sensitive user data (e.g., as defined in Google Play's Data safety section or the relevant privacy regulations).
- MASTG-TEST-0319 — Runtime Use of SDK APIs Known to Handle Sensitive User Data: This test is the dynamic counterpart to @MASTG-TEST-0318.
- MASTG-TEST-0360 — Purpose String Accuracy for Reachable Protected Resource Access: Purpose strings are user-facing explanations that iOS displays when an app requests access to protected resources such as location, camera, microphone, contacts, photos, health data, Bluetooth, motion, or speech recognition. Unlike...
- MASTG-TEST-0361 — Runtime Use of Protected Resource APIs Without Accurate Purpose Strings: This test is the dynamic counterpart to @MASTG-TEST-0360. See @MASTG-TEST-0360 for background on the relationship between protected resources, usage description keys, purpose strings, and framework APIs.
- MASTG-TEST-0362 — Entitlements for Unjustified Capability Exposure: Entitlements are signed rights or privileges that enable an iOS app or app extension to use specific platform services, capabilities, or system integrations. Unlike purpose strings, entitlements are not limited to protected resources or...
- MASTG-TEST-0363 — Runtime Use of Entitlement-Backed APIs for Unjustified Capability Exposure: This test is the dynamic counterpart to @MASTG-TEST-0362. See @MASTG-TEST-0362 for background on the relationship between Xcode capabilities, signed entitlements, and entitlement-backed APIs or entry points.
- MASTG-TEST-0364 — Exported And Unprotected Activities That Expose Sensitive Functionality: If an exported activity does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can start it with an...
- MASTG-TEST-0365 — Exported And Unprotected Services That Expose Sensitive Functionality: If an exported service does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can start or bind to it and...
- MASTG-TEST-0366 — Exported And Unprotected Broadcast Receivers That Expose Sensitive Functionality: If an exported receiver does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can send a broadcast to it...
- MASTG-TEST-0381 — References to Insecure PendingIntent Creation: This test checks for references to `PendingIntent` creation APIs to identify potentially insecure implementations. A `PendingIntent` wraps an `Intent` that will be executed later on behalf of the app's identity and permissions, making...

Mapped MASTG best practices:

- MASTG-BEST-0003 — Comply with Privacy Regulations and Best Practices: Recommendations from CWE-359.
- MASTG-BEST-0045 — Limit Sensitive Data Exposure Through iOS IPC Channels: When your app exchanges data across iOS IPC channels, share the minimum amount of data for the shortest time possible. Design these flows so that intercepted payloads are low value and short lived. Follow the principle of least...
- MASTG-BEST-0051 — Minimize iOS Permissions and Entitlements: Request only the iOS permissions and app capabilities that the app actually needs, and prefer the narrowest Apple-supported access model for each feature. This reduces unnecessary exposure of personal data and limits the blast radius if...
- MASTG-BEST-0052 — Restrict Access to Android App Components: Only export an app component when another app genuinely needs to interact with it. Every exported component is an entry point that other apps on the device may be able to invoke, so keeping components private by default reduces the...
- MASTG-BEST-0056 — Use Explicit Intents for Internal IPC: Use explicit intents when communicating between components within the same app. An explicit intent specifies the target component directly by package name or class name, ensuring the intent can only be delivered to the intended...
- MASTG-BEST-0063 — Use Immutable PendingIntents with Explicit Intents: When creating a `PendingIntent`, always use `FLAG_IMMUTABLE` and ensure the base intent is explicit (targets a specific component).

Mapped MASTG knowledge:

- MASTG-KNOW-0017 — App Permissions: Android assigns a distinct system identity (Linux user ID and group ID) to every installed app. Because each Android app operates in a process sandbox, apps must explicitly request access to resources and data that are outside their...
- MASTG-KNOW-0020 — Inter-Process Communication (IPC) Mechanisms: Every Android process runs in its own sandboxed address space. Inter-process communication (IPC) lets apps and the system exchange data and invoke functionality across these process boundaries. Instead of relying on traditional...
- MASTG-KNOW-0024 — Pending Intents: Often while dealing with complex flows during app development, there are situations where an app A wants another app B to perform a certain action in the future, on app A's behalf. Trying to implement this by only using `Intent`s leads...
- MASTG-KNOW-0026 — Third-party Services Embedded in the App: The features provided by third-party services can involve tracking services to monitor the user's behavior while using the app, selling banner advertisements, or improving the user experience.
- MASTG-KNOW-0077 — App Permissions: iOS permissions work differently from Android. On Android, permissions are declared in a manifest and granted at install time or via runtime prompts. On iOS, access control is a layered model that is worth understanding before diving...
- MASTG-KNOW-0078 — Inter-Process Communication (IPC): iOS does not provide a general-purpose mechanism for third-party apps to communicate directly. Instead, apps exchange data through platform-mediated interfaces of varying levels of abstraction.
- MASTG-KNOW-0132 — Android Activities: An activity is an app component that provides a single screen with a user interface. An app typically implements one activity per screen, so an app with three screens implements three activities. Each activity extends the `Activity`...
- MASTG-KNOW-0133 — Android Services: A service is an app component that performs long-running operations in the background without a user interface, such as processing data, performing network transactions, or interacting with content providers. A service extends the...
- MASTG-KNOW-0134 — Android Broadcast Receivers: A broadcast receiver is an app component that responds to broadcast messages from other apps or from the system. Apps use broadcasts as a publish-subscribe messaging mechanism: the system delivers broadcasts for events such as boot...
