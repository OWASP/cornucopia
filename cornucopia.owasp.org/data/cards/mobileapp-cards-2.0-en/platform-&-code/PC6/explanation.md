## Scenario: Dawn can expose and intercept sensitive functionality through interprocess communication because permissions for broadcast and sharing are not set, not narrow enough or because sensitive functionality isn't appropriately excluded when sharing

### Example

Dawn shares a document from a medical app through a broadcast channel with no narrow permission. A nearby app receives the patient notes and replies with a coupon for orthopedic shoes, demonstrating an enthusiasm nobody requested.

Broadcast and sharing permissions must restrict recipients and exclude sensitive functionality or data when sharing is unnecessary. Loose interprocess permissions expose trusted actions to unrelated applications.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Dawn can expose and intercept sensitive functionality through interprocess communication because permissions for broadcast and sharing are not set, not narrow enough or because sensitive functionality isn't appropriately excluded when sharing.

- **MAS-THREAT-0018:** Attackers can access sensitive data and functionality exposed by app components.
- **MAS-THREAT-0032:** Attackers can intercept or manipulate the app's intents.

- **MAS-ATTACK-0038:** Invoking exported or unprotected app components from another app installed on the device.
- **MAS-ATTACK-0039:** Connecting to open ports or local services exposed by the app.
- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0049:** Registering intent filters to intercept implicit intents sent by the app.
- **MAS-ATTACK-0050:** Modifying or replaying mutable PendingIntents obtained from the app.

### What can go wrong?

If Dawn can expose and intercept sensitive functionality through interprocess communication because permissions for broadcast and sharing are not set, not narrow enough or because sensitive functionality isn't appropriately excluded when sharing, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Invoking exported or unprotected app components from another app installed on the device. Also, Connecting to open ports or local services exposed by the app. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0018 — Lack of Authentication or Authorization on App Components: This weakness occurs when app components that expose functionality or data do not enforce proper authentication or authorization on their callers.
- MASWE-0032 — Insecure Intents: This weakness occurs when an app creates or handles Android intents insecurely, allowing other apps to intercept, redirect, or manipulate its communication.

### What are we going to do about it?

Protect broadcasts and sharing with narrow permissions and explicit recipients, exclude sensitive fields from share payloads, and verify IPC callers before performing privileged work; test malicious receivers, exported components, and alternate share targets.


Mapped MASTG tests:

- MASTG-TEST-0364 — Exported And Unprotected Activities That Expose Sensitive Functionality: If an exported activity does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can start it with an...
- MASTG-TEST-0365 — Exported And Unprotected Services That Expose Sensitive Functionality: If an exported service does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can start or bind to it and...
- MASTG-TEST-0366 — Exported And Unprotected Broadcast Receivers That Expose Sensitive Functionality: If an exported receiver does not define `android:permission` with a proper protection level and performs or grants access to sensitive functionality, another third-party app outside the intended trust boundary can send a broadcast to it...
- MASTG-TEST-0381 — References to Insecure PendingIntent Creation: This test checks for references to `PendingIntent` creation APIs to identify potentially insecure implementations. A `PendingIntent` wraps an `Intent` that will be executed later on behalf of the app's identity and permissions, making...

Mapped MASTG best practices:

- MASTG-BEST-0052 — Restrict Access to Android App Components: Only export an app component when another app genuinely needs to interact with it. Every exported component is an entry point that other apps on the device may be able to invoke, so keeping components private by default reduces the...
- MASTG-BEST-0063 — Use Immutable PendingIntents with Explicit Intents: When creating a `PendingIntent`, always use `FLAG_IMMUTABLE` and ensure the base intent is explicit (targets a specific component).

Mapped MASTG knowledge:

- MASTG-KNOW-0081 — UIActivity Sharing: Starting with iOS 6, apps can share data (items) via the system-wide "Share Sheet" using "Activity Views", which are implemented in the `UIActivityViewController` API.
- MASTG-KNOW-0132 — Android Activities: An activity is an app component that provides a single screen with a user interface. An app typically implements one activity per screen, so an app with three screens implements three activities. Each activity extends the `Activity`...
- MASTG-KNOW-0017 — App Permissions: Android assigns a distinct system identity (Linux user ID and group ID) to every installed app. Because each Android app operates in a process sandbox, apps must explicitly request access to resources and data that are outside their...
- MASTG-KNOW-0020 — Inter-Process Communication (IPC) Mechanisms: Every Android process runs in its own sandboxed address space. Inter-process communication (IPC) lets apps and the system exchange data and invoke functionality across these process boundaries. Instead of relying on traditional...
- MASTG-KNOW-0133 — Android Services: A service is an app component that performs long-running operations in the background without a user interface, such as processing data, performing network transactions, or interacting with content providers. A service extends the...
- MASTG-KNOW-0134 — Android Broadcast Receivers: A broadcast receiver is an app component that responds to broadcast messages from other apps or from the system. Apps use broadcasts as a publish-subscribe messaging mechanism: the system delivers broadcasts for events such as boot...
