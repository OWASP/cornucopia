## Scenario: Xavier can inject scripts into the web view because it allows embedding content using deep linking without proper authorization and validation of the host, schema and path of the target as these can be changed by the user or because safe browsing is disabled

### Example

Xavier follows a deep link from a message into a WebView. The link changes its host and path to an attacker page, injects script into the view, and offers Xavier a button to “claim complimentary internet.”

Deep links must allowlist scheme, host, and path, authorize the destination, and use safe browsing protections. Otherwise user-controlled navigation can place attacker content inside a privileged web view.


## Threat Modeling

### STRIDE

This scenario is primarily **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Xavier can inject scripts into the web view because it allows embedding content using deep linking without proper authorization and validation of the host, schema and path of the target as these can be changed by the user or because safe browsing is disabled.

- **MAS-THREAT-0035:** Attackers can execute malicious web content inside the app's WebView.
- **MAS-THREAT-0034:** Attackers can access local files and app-private data from web content.
- **MAS-THREAT-0029:** Attackers can hijack deep links or inject malicious input into the app.

- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0051:** Injecting malicious JavaScript into WebView content (e.g., via MITM on insecure connections or a compromised website).
- **MAS-ATTACK-0046:** Registering the same custom URL scheme to intercept links intended for the app.

### What can go wrong?

If Xavier can inject scripts into the web view because it allows embedding content using deep linking without proper authorization and validation of the host, schema and path of the target as these can be changed by the user or because safe browsing is disabled, the failure is concrete rather than merely theatrical: the app could let an attacker cross the platform-&-code boundary and reach data or capability that this flow should protect. In this card, the practical route includes Delivering crafted deep links or intents from a malicious app or web page. Also, Injecting malicious JavaScript into WebView content (e.g., via MITM on insecure connections or a compromised website). That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0035 — WebViews Loading Untrusted Content: This weakness occurs when a WebView loads URLs, HTML, or JavaScript from untrusted sources, or lets users navigate to arbitrary sites outside the developer's control.
- MASWE-0034 — WebViews Allow Access to Local Resources with Untrusted Content: This weakness occurs when a WebView is configured to access local resources while also rendering untrusted content, allowing that content to reach files and data outside the web sandbox.
- MASWE-0029 — Insecure Deep Links: This weakness occurs when an app handles deep links insecurely, relying on unverified schemes or trusting the attacker-controllable data they carry.

### What are we going to do about it?

Allow WebView navigation only to approved HTTPS schemes, hosts, and paths, validate deep links before loading them, enable Safe Browsing, and restrict JavaScript bridges and file access; test hostile URLs, redirects, injected scripts, and untrusted origins.


Mapped MASTG tests:

- MASTG-TEST-0332 — Attacker-Controlled URI in WebViews: iOS apps can dynamically load content into a `WKWebView` using various URL load methods. These methods can render both remote web content and locally stored files.
- MASTG-TEST-0333 — Overly Broad File Read Access in WebViews: iOS apps can load local files into a `WKWebView` using `loadFileURL(_:allowingReadAccessTo:)`).
- MASTG-TEST-0335 — WebView File Origin Access Relaxed by Configuration: `WKWebView` supports configuration that affects how JavaScript running from `file://` origins can access other resources. In particular, `allowFileAccessFromFileURLs` allows JavaScript running in the context of a `file://` URL to access...
- MASTG-TEST-0336 — Runtime Setting of Relaxed WebView File Origin Policies: This test is the dynamic counterpart to @MASTG-TEST-0335.
- MASTG-TEST-0370 — Missing Input Validation in Custom URL Scheme Handlers: Apps that register custom URL schemes must validate and sanitize all URL parameters before using them in security-sensitive operations (@MASTG-KNOW-0079). Without input validation, any caller that opens a registered URL scheme can...
- MASTG-TEST-0371 — Missing Source Validation in Custom URL Scheme Handlers: Custom URL scheme handlers that perform security-sensitive operations should validate the source application before acting on incoming requests (@MASTG-KNOW-0079). The `sourceApplication` property provides the bundle ID of the calling...
- MASTG-TEST-0393 — Use of Unverified App Links: Android App Links are `http`/`https` deep links that the OS verifies against a website's Digital Asset Links file before routing them to the app. An app opts into this verification by setting `android:autoVerify="true"` on the...
- MASTG-TEST-0394 — Missing Input Validation in Custom URL Scheme Handlers: Apps register custom URL schemes by declaring an `<intent-filter>` in the `AndroidManifest.xml` with an `<action android:name="android.intent.action.VIEW">`, the `android.intent.category.BROWSABLE` category, and a `<data>` element whose...
- MASTG-TEST-0395 — Missing Input Validation in Universal Link Handlers: Apps that support universal links must validate and sanitize the path and query parameters of the incoming URL before using them in security-sensitive operations (@MASTG-KNOW-0080). iOS verifies the link's **domain** against the...
- MASTG-TEST-0398 — References to WebViewClient URL Loading Handlers: This test checks for references to `WebViewClient` URL interception methods that override the default page navigation behavior in WebViews. The default and safest behavior on Android is to let the default web browser open any link that...
- MASTG-TEST-0399 — SafeBrowsing Disabled: This test checks whether the SafeBrowsing API is explicitly disabled, either in the AndroidManifest.xml or in the WebView code. Since Android 8.1 (API level 27), WebViews include SafeBrowsing by default, which warns users about URLs...
- MASTG-TEST-0400 — Runtime Use of WebViewClient URL Loading Handlers: This test dynamically analyzes the runtime behavior of `WebViewClient` URL interception methods to understand how the app handles URL loading in WebViews. By hooking relevant methods at runtime, you can observe:

Mapped MASTG best practices:

- MASTG-BEST-0034 — Validate WebView Input: Always treat any data passed to a `WKWebView` as untrusted unless it is fully controlled by the app. This includes URLs loaded through `load(_:)`), local files loaded through `loadFileURL`), HTML passed to `loadHTMLString`), JavaScript...
- MASTG-BEST-0033 — Securely Load File Content in a WebView: For `WKWebView`, `allowFileAccessFromFileURLs` and `allowUniversalAccessFromFileURLs` are not part of the public iOS `WKWebView` API. They are commonly accessed through Key-Value Coding (KVC), but should remain disabled unless there is...
- MASTG-BEST-0045 — Limit Sensitive Data Exposure Through iOS IPC Channels: When your app exchanges data across iOS IPC channels, share the minimum amount of data for the shortest time possible. Design these flows so that intercepted payloads are low value and short lived. Follow the principle of least...
- MASTG-BEST-0054 — Validate Input Parameters in Custom URL Scheme Handlers: Validate and sanitize all URL parameters before using them in your custom URL scheme handler. Since any app on the device can open a custom URL scheme, treat all incoming parameter values as untrusted input.
- MASTG-BEST-0055 — Validate Source Application in Custom URL Scheme Handlers: When a custom URL scheme triggers a privileged or irreversible action, check `sourceApplication` from `UIOpenURLContext.options` before processing the request. This allows you to verify the calling app's bundle ID against an allowlist.
- MASTG-BEST-0070 — Verify Android App Links with autoVerify and Digital Asset Links: When your app handles `http`/`https` deep links, declare them as Android App Links so the OS verifies that your app owns the target domain. Without verification, any other app can register the same intent filter and intercept the links...
- MASTG-BEST-0071 — Validate Input Parameters in Deep Link and Custom URL Scheme Handlers: Validate and sanitize every value read from an incoming deep link before using it. Any app on the device can send an Intent that targets your handler, and Android provides no reliable way to identify the caller, so treat all parameters...
- MASTG-BEST-0072 — Validate Input Parameters in Universal Link Handlers: Validate and sanitize the path and query parameters of every incoming universal link before using them in security-sensitive operations. Universal link verification only proves that the request targets a domain your app is associated...

Mapped MASTG knowledge:

- MASTG-KNOW-0076 — WebViews: WebViews are in-app browser components for displaying interactive web content. They can be used to embed web content directly into an app's user interface. iOS WebViews execute JavaScript and render HTML, and therefore can execute...
- MASTG-KNOW-0079 — Custom URL Schemes: Custom URL schemes allow iOS apps to receive requests from other apps or web pages via a custom URI protocol (for example, `myapp://action?param=value`). An app declares the schemes it handles and processes incoming URLs through...
- MASTG-KNOW-0019 — Deep Links: _Deep links_ are URIs of any scheme that take users directly to specific content in an app. An app can set up deep links by adding _intent filters_ on the Android Manifest and extracting data from incoming intents to navigate users to...
- MASTG-KNOW-0080 — Universal Links: Universal links are the iOS equivalent to Android App Links (aka. Digital Asset Links) and are used for deep linking. When tapping a universal link (to the app's website), the user will seamlessly be redirected to the corresponding...
- MASTG-KNOW-0018 — WebViews: On Android versions prior to 4.4, WebViews used the WebKit rendering engine to display web pages. Since Android 4.4, WebViews have been based on Chromium, providing improved performance and compatibility. However, the pages are still...
