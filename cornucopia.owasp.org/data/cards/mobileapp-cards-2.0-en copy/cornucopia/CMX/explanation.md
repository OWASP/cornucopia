## Scenario: Roxana can do arbitrary file overwrites and potentially execute malicious code through path traversal because the target path and directory is not appropriately validated

### Example

Roxana uploads a photo to a community printer, entering `..\..\shared\orders\invoice.csv` as the filename. The printer overwrites the office invoice and then reports that her landscape photo has been “financially developed.”

User-controlled path components must be constrained to an approved directory and safe generated names. Without canonicalization and containment checks, traversal can overwrite arbitrary files and may place executable content where the system will run it.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering** in STRIDE. The named condition is: Roxana can do arbitrary file overwrites and potentially execute malicious code through path traversal because the target path and directory is not appropriately validated.

- **MAS-THREAT-0029:** Attackers can hijack deep links or inject malicious input into the app.

- **MAS-ATTACK-0046:** Registering the same custom URL scheme to intercept links intended for the app.
- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.

### What can go wrong?

If Roxana can do arbitrary file overwrites and potentially execute malicious code through path traversal because the target path and directory is not appropriately validated, the failure is concrete rather than merely theatrical: the app could let an attacker cross the cornucopia boundary and reach data or capability that this flow should protect. In this card, the practical route includes Registering the same custom URL scheme to intercept links intended for the app. Also, Delivering crafted deep links or intents from a malicious app or web page. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0029 — Insecure Deep Links: This weakness occurs when an app handles deep links insecurely, relying on unverified schemes or trusting the attacker-controllable data they carry.

### What are we going to do about it?

Canonicalize and allowlist every file path, reject absolute paths, traversal, and symlinks, and generate storage names rather than trusting user filenames; test encoded traversal and containment before opening or overwriting any file.


Mapped MASTG tests:

- MASTG-TEST-0370 — Missing Input Validation in Custom URL Scheme Handlers: Apps that register custom URL schemes must validate and sanitize all URL parameters before using them in security-sensitive operations (@MASTG-KNOW-0079). Without input validation, any caller that opens a registered URL scheme can...
- MASTG-TEST-0394 — Missing Input Validation in Custom URL Scheme Handlers: Apps register custom URL schemes by declaring an `<intent-filter>` in the `AndroidManifest.xml` with an `<action android:name="android.intent.action.VIEW">`, the `android.intent.category.BROWSABLE` category, and a `<data>` element whose...
- MASTG-TEST-0395 — Missing Input Validation in Universal Link Handlers: Apps that support universal links must validate and sanitize the path and query parameters of the incoming URL before using them in security-sensitive operations (@MASTG-KNOW-0080). iOS verifies the link's **domain** against the...

Mapped MASTG best practices:

- MASTG-BEST-0045 — Limit Sensitive Data Exposure Through iOS IPC Channels: When your app exchanges data across iOS IPC channels, share the minimum amount of data for the shortest time possible. Design these flows so that intercepted payloads are low value and short lived. Follow the principle of least...
- MASTG-BEST-0054 — Validate Input Parameters in Custom URL Scheme Handlers: Validate and sanitize all URL parameters before using them in your custom URL scheme handler. Since any app on the device can open a custom URL scheme, treat all incoming parameter values as untrusted input.
- MASTG-BEST-0071 — Validate Input Parameters in Deep Link and Custom URL Scheme Handlers: Validate and sanitize every value read from an incoming deep link before using it. Any app on the device can send an Intent that targets your handler, and Android provides no reliable way to identify the caller, so treat all parameters...
- MASTG-BEST-0072 — Validate Input Parameters in Universal Link Handlers: Validate and sanitize the path and query parameters of every incoming universal link before using them in security-sensitive operations. Universal link verification only proves that the request targets a domain your app is associated...

Mapped MASTG knowledge:

- MASTG-KNOW-0079 — Custom URL Schemes: Custom URL schemes allow iOS apps to receive requests from other apps or web pages via a custom URI protocol (for example, `myapp://action?param=value`). An app declares the schemes it handles and processes incoming URLs through...
- MASTG-KNOW-0019 — Deep Links: _Deep links_ are URIs of any scheme that take users directly to specific content in an app. An app can set up deep links by adding _intent filters_ on the Android Manifest and extracting data from incoming intents to navigate users to...
- MASTG-KNOW-0080 — Universal Links: Universal links are the iOS equivalent to Android App Links (aka. Digital Asset Links) and are used for deep linking. When tapping a universal link (to the app's website), the user will seamlessly be redirected to the corresponding...
