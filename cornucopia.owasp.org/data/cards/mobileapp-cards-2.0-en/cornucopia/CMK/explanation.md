## Scenario: Ruben can use the app to spread malicious code because it accepts, loads, or forwards untrusted content without verifying its source, type, or safety

### Example

Ruben runs a community radio app that accepts an audio “theme pack” from anyone. A listener uploads a file that secretly carries executable content, and the station’s playlist begins broadcasting a loop of the mayor’s duck impression.

Untrusted content must be checked for source, type, and safety before the app loads or forwards it. Otherwise a convenient sharing feature becomes a distribution channel for malicious code.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Ruben can use the app to spread malicious code because it accepts, loads, or forwards untrusted content without verifying its source, type, or safety.

- **MAS-THREAT-0050:** Attackers can execute injection attacks against the app.

- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0059:** Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals).

### What can go wrong?

If Ruben can use the app to spread malicious code because it accepts, loads, or forwards untrusted content without verifying its source, type, or safety, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Delivering crafted deep links or intents from a malicious app or web page. Also, Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals). That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0050 — Unsafe Handling of Untrusted Data: This weakness occurs when data originating outside the app's trust boundary reaches a sensitive sink without being validated, sanitized, or safely parsed.

### What are we going to do about it?

Accept, load, or forward content only from allowlisted sources and types, verify signatures or hashes, and keep it in a sandbox without dynamic execution; test malformed packages, untrusted WebView content, and dependency substitution.


Mapped MASTG tests:

- MASTG-TEST-0375 — Missing Validation of Data Returned from Implicit Intents: An implicit intent is an `Intent` that does not name a concrete target component. Instead, it declares an action, and optionally data or categories, and Android resolves it to an installed component with a matching `<intent-filter>`....

Mapped MASTG best practices:

- MASTG-BEST-0057 — Sanitize Data Coming from External Components: All data received from external sources (such as `Intent` extras, activity results, or `ContentProvider` results) must be treated as untrusted and thoroughly sanitized before use. Failure to validate this data can lead to serious...

Mapped MASTG knowledge:

- MASTG-KNOW-0081 — UIActivity Sharing: Starting with iOS 6, apps can share data (items) via the system-wide "Share Sheet" using "Activity Views", which are implemented in the `UIActivityViewController` API.
- MASTG-KNOW-0025 — Explicit vs Implicit Intents: An `Intent` is a messaging object used to request an action from another app component. Intents support three fundamental use cases: starting an activity, starting a service, and delivering a broadcast. See @MASTG-KNOW-0020 for the...
- MASTG-KNOW-0138 — URI Schemes in Android Intent Results: When an activity requests content from another app and receives a result, the responding activity returns data via `setResult`). Legacy code commonly receives that result through `onActivityResult`); newer code uses the Activity Result...
