## Scenario: Matteo can bypass access controls and trigger functionality because debugging is left enabled in the production build

### Example

Matteo leaves a production tablet’s debug port enabled. A curious airport kiosk technician attaches a laptop, invokes an internal command, and makes the tablet print boarding passes for a flock of imaginary frequent flyers.

Debugging facilities must be disabled or tightly controlled in release builds. An exposed debugger can invoke privileged functionality and bypass the access checks ordinary users encounter.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Information Disclosure** in STRIDE. The named condition is: Matteo can bypass access controls and trigger functionality because debugging is left enabled in the production build.

- **MAS-THREAT-0063:** Attackers can inspect and manipulate a debuggable app at runtime, even on non-rooted or non-jailbroken devices.

- **MAS-ATTACK-0002:** Debugging the app at runtime.
- **MAS-ATTACK-0003:** Using dynamic instrumentation.
- **MAS-ATTACK-0004:** Attaching a remote inspector to the app's debuggable web content.

### What can go wrong?

If Matteo can bypass access controls and trigger functionality because debugging is left enabled in the production build, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Debugging the app at runtime. Also, Using dynamic instrumentation. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0063 — Debug Mechanisms Not Disabled: This weakness occurs when the application has debug mechanisms enabled in production builds, allowing the usage of platform debuggers, or exposes embedded web or JavaScript content to developer inspection tools.

### What are we going to do about it?

Disable debuggable flags, debugger waits, and test hooks in release builds, and gate sensitive actions on server-side checks where possible; verify with runtime debugging and component-access tests that a debugger cannot bypass controls.


Mapped MASTG tests:

- MASTG-TEST-0226 — Debuggable Flag Enabled in the AndroidManifest: This test case checks if the app has the `debuggable` flag (`android:debuggable`) set to `true` in the `AndroidManifest.xml`. When this flag is enabled, it allows the app to be debugged enabling attackers to inspect the app's internals,...
- MASTG-TEST-0227 — Debugging Enabled for WebViews: The `WebView.setWebContentsDebuggingEnabled(true)` API enables debugging for **all** WebViews in the application. This feature can be useful during development, but introduces significant security risks if left enabled in production....
- MASTG-TEST-0261 — Debuggable Entitlement Enabled in the entitlements.plist: The test evaluates whether an iOS application is configured to allow debugging. If an app is debuggable, attackers can leverage debugging tools (see @MASTG-TECH-0084) to analyse the runtime behaviour of the app, and potentially...

Mapped MASTG best practices:

- MASTG-BEST-0007 — Debuggable Flag Disabled in the AndroidManifest: Ensure the debuggable flag in the AndroidManifest.xml is set to `false` for all release builds.
- MASTG-BEST-0008 — Debugging Disabled for WebViews: Ensure that WebView debugging is disabled in production builds to prevent attackers from exploiting this feature to eavesdrop, modify, or debug communication within WebViews.

Mapped MASTG knowledge:

- MASTG-KNOW-0007 — Debuggable Apps: Debugging is an essential process for developers to identify and fix errors or bugs in their Android app. By using a debugger, developers can select the device to debug their app on and set breakpoints in their Java, Kotlin, and C/C++...
- MASTG-KNOW-0028 — Anti-Debugging: Debugging is a highly effective way to analyze runtime app behavior. It allows the reverse engineer to step through the code, stop app execution at arbitrary points, inspect the state of variables, read and modify memory, and a lot more.
- MASTG-KNOW-0062 — Debuggable Apps: Apps can be made debuggable (@MASTG-TECH-0031) by adding the `get-task-allow` key to the app entitlements file and setting it to `true`.
