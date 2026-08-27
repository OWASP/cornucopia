## Scenario: Harold can expose sensitive data displayed, entered, or cached because the data is excessive, not properly masked or cleared after use, persisted without protection, exposed to web content, or made available to third-party components through unnecessary permissions

### Example

Harold books a doctor’s appointment while an app leaves the full diagnosis in a screenshot, cache, and embedded web page. His phone’s lock screen then displays enough detail for the bus driver to ask whether Harold has considered a second opinion.

Sensitive data should be minimized, masked, cleared after use, and kept away from unnecessary web or third-party access. Excess copies and permissive components turn an ordinary appointment into a public announcement.


## Threat Modeling

### STRIDE

This scenario is primarily **Information Disclosure**, **Elevation of Privilege** in STRIDE. The named condition is: Harold can expose sensitive data displayed, entered, or cached because the data is excessive, not properly masked or cleared after use, persisted without protection, exposed to web content, or made available to third-party components through unnecessary permissions.

- **MAS-THREAT-0036:** Attackers can capture sensitive data displayed or entered in the user interface.
- **MAS-THREAT-0001:** Attackers can access sensitive data stored unencrypted in private storage.
- **MAS-THREAT-0034:** Attackers can access local files and app-private data from web content.
- **MAS-THREAT-0066:** Apps and embedded third-party components can access more sensitive device resources and data than needed.

- **MAS-ATTACK-0005:** Accessing the device storage on a compromised device.
- **MAS-ATTACK-0041:** Reading sensitive data from the clipboard when users copy it between apps.
- **MAS-ATTACK-0043:** Observing the device screen while sensitive data is displayed or entered (shoulder surfing).
- **MAS-ATTACK-0007:** Accessing files exposed through incorrect file permissions or misconfigured content providers.
- **MAS-ATTACK-0008:** Extracting local or cloud backups of the device.
- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0051:** Injecting malicious JavaScript into WebView content (e.g., via MITM on insecure connections or a compromised website).
- **MAS-ATTACK-0088:** Holding excessive or no-longer-needed permissions granted to the app.
- **MAS-ATTACK-0089:** Using permissions granted to the host app to call protected APIs and collect data from a third-party SDK.

### What can go wrong?

If Harold can expose sensitive data displayed, entered, or cached because the data is excessive, not properly masked or cleared after use, persisted without protection, exposed to web content, or made available to third-party components through unnecessary permissions, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Accessing the device storage on a compromised device. Also, Reading sensitive data from the clipboard when users copy it between apps. That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0036 — Unnecessary Exposure of Sensitive Data via the User Interface: This weakness occurs when an app exposes sensitive data beyond what is required for the user's current task, or exposes required data without protections proportionate to its sensitivity through its user interface.
- MASWE-0001 — Sensitive Data Stored Unencrypted in Private Storage: This weakness occurs when an app stores sensitive data unencrypted in private storage locations, such as the application sandbox, where it can be exposed via incorrect file permissions, an app or device vulnerability, or data backup...
- MASWE-0034 — WebViews Allow Access to Local Resources with Untrusted Content: This weakness occurs when a WebView is configured to access local resources while also rendering untrusted content, allowing that content to reach files and data outside the web sandbox.
- MASWE-0066 — Inadequate Permission Management: This weakness occurs when an app requests more permissions than it needs, keeps permissions it no longer needs, or fails to explain why permissions are required.

### What are we going to do about it?

Minimize and mask sensitive UI data, use secure text fields and screen-redaction or screenshot-prevention controls, clean WebView storage, keep sensitive entry in native views, and request only permissions needed for the task; test screenshots, clipboard, WebView, and custom-keyboard exposure.


Mapped MASTG tests:

- MASTG-TEST-0316 — App Exposing User Authentication Data in Text Input Fields: This test verifies that the app handles user input correctly, ensuring that access codes (passwords or pins) and verification codes (OTPs) are not exposed in plain text within text input fields.
- MASTG-TEST-0320 — WebViews Not Cleaning Up Sensitive Data: This test verifies whether the app cleans up sensitive data used by WebViews. Apps can enable several specific storage areas in their WebViews and not clean them up properly, leading to sensitive data being stored on the device longer...
- MASTG-TEST-0346 — References to APIs Hiding Sensitive Data in Text Input Fields: If the app does not mask text input fields that contain sensitive data, such data may be visible to bystanders (shoulder surfing) or captured in screenshots and screen recordings. Marking a field as secure also keeps it on the system...
- MASTG-TEST-0347 — Runtime Use of APIs Hiding Sensitive Data in Text Input Fields: This test complements @MASTG-TEST-0346. It monitors text input fields in the app at runtime to check if the app masks the text entry when the user enters sensitive data.
- MASTG-TEST-0378 — References to Password Fields in WebView-Loaded HTML: When an iOS app renders HTML containing `<input type="password">` elements inside a `WKWebView`, any JavaScript running on the page, including injected XSS payloads and third-party scripts loaded by the page, can read the typed value...
- MASTG-TEST-0390 — Full Access Requested by a Custom Keyboard Extension: A custom keyboard is an app extension that replaces the system keyboard across all apps on the device (see @MASTG-KNOW-0141). By default it runs without "Full Access", which keeps it from making network requests or reaching shared...

Mapped MASTG best practices:

- MASTG-BEST-0028 — WebViews Cache Cleanup: Android WebViews cache data when the server responds with specific `Cache-Control` headers that instruct the browser to cache the content. If a WebView processes sensitive data, you should ensure that no residual information remains on...
- MASTG-BEST-0044 — Mask Sensitive Data in Text Input Fields: For any text input field that handles sensitive information such as passwords, PINs, or OTPs, ensure that the entered text is visually masked to prevent bystanders or screen capture tools from exposing it.
- MASTG-BEST-0059 — Render Sensitive UI as Native Views Over the WebView: When a `WKWebView` needs to present sensitive UI, such as a credential picker, autofill suggestion, or payment confirmation, rendering that interface as HTML elements inside the WebView exposes it to any JavaScript running on the page....
- MASTG-BEST-0060 — Use Native Views for Sensitive Text Entry Over a WebView: When a `WKWebView` contains an HTML `<input type="password">` or any sensitive text field, the typed value is stored in the element's `.value` property. Any JavaScript running on the page, including injected XSS payloads, can read it...
- MASTG-BEST-0069 — Keep Sensitive Input on the System Keyboard: Custom keyboards are app extensions that replace the system keyboard across all apps and, once granted "Full Access", can transmit what the user types off the device (see @MASTG-KNOW-0082). For input that carries secrets, such as...

Mapped MASTG knowledge:

- MASTG-KNOW-0018 — WebViews: On Android versions prior to 4.4, WebViews used the WebKit rendering engine to display web pages. Since Android 4.4, WebViews have been based on Chromium, providing improved performance and compatibility. However, the pages are still...
- MASTG-KNOW-0121 — Text Input Field Masking in iOS: iOS provides dedicated APIs to mask text entered in input fields, replacing visible characters with bullet characters. This helps prevent entered text from being observed on-screen by bystanders, shoulder surfing, and may help protect...
- MASTG-KNOW-0141 — Custom Keyboards: A custom keyboard is an app extension (see @MASTG-KNOW-0082) that replaces the system keyboard across all apps on the device. The user installs it through its containing app and must explicitly enable it in **Settings** (**General >...
- MASTG-KNOW-0076 — WebViews: WebViews are in-app browser components for displaying interactive web content. They can be used to embed web content directly into an app's user interface. iOS WebViews execute JavaScript and render HTML, and therefore can execute...
- MASTG-KNOW-0139 — WKContentWorld: `WKContentWorld`, introduced in iOS 14, represents an isolated JavaScript execution environment within a `WKWebView`. Each content world has its own JavaScript global scope and its own copy of the built-in prototype chain, but all...
- MASTG-KNOW-0082 — App Extensions: Starting with iOS 8, Apple introduced App Extensions. App extensions let an app offer custom functionality and content to users while they interact with other apps or the system. Each extension implements a single, well-scoped task, for...
