## Scenario: Sebastien can disclose sensitive data or internal behavior because debug code, verbose diagnostics, test resources, or unsafe runtime logging remain in the production app

### Example

Sebastien presents an app at work while verbose logs print customer addresses across the projector like an accidental office mural. A colleague jokes that the quarterly roadmap now includes everyone’s home address.

Production builds should remove debug paths, test resources, and unsafe logging of sensitive values. Diagnostics that reveal internal behavior or personal data turn a routine demonstration into an information leak.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure** in STRIDE. The named condition is: Sebastien can disclose sensitive data or internal behavior because debug code, verbose diagnostics, test resources, or unsafe runtime logging remain in the production app.

- **MAS-THREAT-0061:** Attackers can analyze the app's internals and disable its security controls.

- **MAS-ATTACK-0001:** Obtaining the app package and reverse engineering it.
- **MAS-ATTACK-0006:** Accessing the system logs on a compromised device or from an app holding log-access permissions.

### What can go wrong?

If Sebastien can disclose sensitive data or internal behavior because debug code, verbose diagnostics, test resources, or unsafe runtime logging remain in the production app, the failure is concrete rather than merely theatrical: the app could let an attacker cross the resilience boundary and reach data or capability that this flow should protect. In this card, the practical route includes Obtaining the app package and reverse engineering it. Also, Accessing the system logs on a compromised device or from an app holding log-access permissions. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0061 — Debug Artifacts Not Removed: This weakness occurs when an app ships to production containing developer debug artifacts, such as verbose logging, testing utilities, debugging symbols, or leftover debug and test code.

### What are we going to do about it?

Remove debug code, test resources, StrictMode penalties, verbose logging, and sensitive values from production builds; inspect release logs and package contents and run the mapped static and runtime logging tests to confirm diagnostics reveal no internals.


Mapped MASTG tests:

- MASTG-TEST-0263 — Logging of StrictMode Violations: This test checks whether an app enables `StrictMode` in production. While useful for developers to log policy violations such as disk I/O or network operations in production apps, leaving `StrictMode` enabled can expose sensitive...
- MASTG-TEST-0264 — Runtime Use of StrictMode APIs: This test checks whether the app uses `StrictMode` by dynamically analyzing the app's behavior and placing relevant hooks to detect the use of `StrictMode` APIs, such as `StrictMode.setVmPolicy` and `StrictMode.VmPolicy.Builder.penaltyLog`.
- MASTG-TEST-0265 — References to StrictMode APIs: This test checks whether the app uses `StrictMode`. While useful for developers to log policy violations such as disk I/O or network operations during development, it can expose sensitive implementation details in the logs that could be...
- MASTG-TEST-0358 — Implementation Details Exposure Through Logging APIs: This test checks for verbose error logging and debugging messages in iOS applications. While logging is useful during development, verbose logging in production builds can expose implementation details such as function names, code...
- MASTG-TEST-0359 — Implementation Details Exposure in Logs: This test is the dynamic counterpart to @MASTG-TEST-0358.

Mapped MASTG best practices:

- MASTG-BEST-0022 — Disable Verbose and Debug Logging in Production Builds: When logging information, it's crucial to protect sensitive values and avoid exposing unnecessary implementation details.

Mapped MASTG knowledge:

- MASTG-KNOW-0064 — Non-Production Resources: Non-production resources are assets, endpoints, or configurations intended for development, testing, or staging environments rather than live production use. These resources often have relaxed security controls, debug features, or test...
- MASTG-KNOW-0101 — Logs: Logging is commonly used during development and troubleshooting to record runtime behavior, errors, and operational events. Depending on what is recorded, logs may include request/response metadata, identifiers, stack traces, and other...
