## Scenario: Toby can modify or expose data because intents are implicit, contains security-relevant data which apps can register for, or because the response from the intents is not properly validated or sanitized

### Example

Toby taps a restaurant app’s implicit “send order” intent, which another app has registered to intercept. The interceptor changes “one soup” to “one hundred soups,” and the waiter wheels in a tureen large enough to require planning permission.

Sensitive intents need explicit destinations, minimal data, and strict validation of returned values. An untrusted app can otherwise alter or read the message while pretending to be a helpful recipient.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Toby can modify or expose data because intents are implicit, contains security-relevant data which apps can register for, or because the response from the intents is not properly validated or sanitized.

- **MAS-THREAT-0032:** Attackers can intercept or manipulate the app's intents.
- **MAS-THREAT-0050:** Attackers can execute injection attacks against the app.

- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0049:** Registering intent filters to intercept implicit intents sent by the app.
- **MAS-ATTACK-0050:** Modifying or replaying mutable PendingIntents obtained from the app.
- **MAS-ATTACK-0059:** Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals).

### What can go wrong?

If Toby can modify or expose data because intents are implicit, contains security-relevant data which apps can register for, or because the response from the intents is not properly validated or sanitized, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Delivering crafted deep links or intents from a malicious app or web page. Also, Registering intent filters to intercept implicit intents sent by the app. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0032 — Insecure Intents: This weakness occurs when an app creates or handles Android intents insecurely, allowing other apps to intercept, redirect, or manipulate its communication.
- MASWE-0050 — Unsafe Handling of Untrusted Data: This weakness occurs when data originating outside the app's trust boundary reaches a sensitive sink without being validated, sanitized, or safely parsed.

### What are we going to do about it?

Use explicit, immutable intents for sensitive operations, restrict receivers with signature-level permissions, allowlist actions and destinations, and validate and sanitize every returned extra before changing state; test crafted intents and unexpected responses.


Mapped MASTG tests:

- MASTG-TEST-0372 — Implicit Intents Used for Internal App Communication: An implicit intent is an `Intent` that does not name a concrete target component. Instead, it declares an action, and optionally data or categories, and Android resolves it to an installed component with a matching `<intent-filter>`....
- MASTG-TEST-0374 — References to Implicit Intents Carrying Sensitive Extras: An implicit intent is an `Intent` that does not name a concrete target component. Instead, it declares an action, and optionally data or categories, and Android resolves it to an installed component with a matching `<intent-filter>`....
- MASTG-TEST-0375 — Missing Validation of Data Returned from Implicit Intents: An implicit intent is an `Intent` that does not name a concrete target component. Instead, it declares an action, and optionally data or categories, and Android resolves it to an installed component with a matching `<intent-filter>`....

Mapped MASTG best practices:

- MASTG-BEST-0056 — Use Explicit Intents for Internal IPC: Use explicit intents when communicating between components within the same app. An explicit intent specifies the target component directly by package name or class name, ensuring the intent can only be delivered to the intended...
- MASTG-BEST-0057 — Sanitize Data Coming from External Components: All data received from external sources (such as `Intent` extras, activity results, or `ContentProvider` results) must be treated as untrusted and thoroughly sanitized before use. Failure to validate this data can lead to serious...

Mapped MASTG knowledge:

- MASTG-KNOW-0025 — Explicit vs Implicit Intents: An `Intent` is a messaging object used to request an action from another app component. Intents support three fundamental use cases: starting an activity, starting a service, and delivering a broadcast. See @MASTG-KNOW-0020 for the...
- MASTG-KNOW-0138 — URI Schemes in Android Intent Results: When an activity requests content from another app and receives a result, the responding activity returns data via `setResult`). Legacy code commonly receives that result through `onActivityResult`); newer code uses the Activity Result...
