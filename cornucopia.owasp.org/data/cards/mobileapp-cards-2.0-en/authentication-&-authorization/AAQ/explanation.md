## Scenario: Riotaro can bypass authorization controls by exploiting data flows between views, processes, and components to inject commands, manipulate data, or disclose sensitive information

### Example

Riotaro volunteers backstage at a school play, where a lighting tablet passes scene details through a shared message bus. He slips “open payroll and add 400 gold stars” into the handoff, and the treasurer’s screen dutifully awards the cast a mythical bonus.

The receiving component accepts a command merely because it arrived through a neighboring component. Data flowing between views, processes, and services needs authorization and validation at each boundary, or a crafted message can trigger sensitive actions or expose their results.


## Threat Modeling

### STRIDE

This scenario is primarily **Spoofing**, **Tampering**, **Information Disclosure** in STRIDE. The named condition is: Riotaro can bypass authorization controls by exploiting data flows between views, processes, and components to inject commands, manipulate data, or disclose sensitive information.

- **MAS-THREAT-0034:** Attackers can access local files and app-private data from web content.
- **MAS-THREAT-0050:** Attackers can execute injection attacks against the app.

- **MAS-ATTACK-0047:** Delivering crafted deep links or intents from a malicious app or web page.
- **MAS-ATTACK-0051:** Injecting malicious JavaScript into WebView content (e.g., via MITM on insecure connections or a compromised website).
- **MAS-ATTACK-0059:** Supplying crafted input through any external interface (network, IPC, files, UI, or peripherals).

### What can go wrong?

If Riotaro can bypass authorization controls by exploiting data flows between views, processes, and components to inject commands, manipulate data, or disclose sensitive information, the failure is concrete rather than merely theatrical: the app could let an attacker cross the authentication-&-authorization boundary and reach data or capability that this flow should protect. In this card, the practical route includes Delivering crafted deep links or intents from a malicious app or web page. Also, Injecting malicious JavaScript into WebView content (e.g., via MITM on insecure connections or a compromised website). That can turn a normal user action into unauthorized access, disclosure, alteration, or service disruption; the mapped weakness entries below identify the exact implementation evidence to check.

Mapped weaknesses that sharpen the review:

- MASWE-0034 — WebViews Allow Access to Local Resources with Untrusted Content: This weakness occurs when a WebView is configured to access local resources while also rendering untrusted content, allowing that content to reach files and data outside the web sandbox.
- MASWE-0050 — Unsafe Handling of Untrusted Data: This weakness occurs when data originating outside the app's trust boundary reaches a sensitive sink without being validated, sanitized, or safely parsed.

### What are we going to do about it?

Treat every cross-component value as untrusted: use explicit, immutable intents and narrowly scoped IPC permissions, validate deep-link and WebView inputs against an allowlist, and test that crafted messages cannot invoke or disclose privileged data.


Mapped MASTG tests:

- MASTG-TEST-0334 — Native Code Exposed Through WebViews: This test verifies Android apps that use WebViews with legacy WebView-Native bridges do not expose native code to websites loaded inside the WebView.
- MASTG-TEST-0339 — SQL Injection in Content Providers: Android applications can share structured data via `ContentProvider` components. However, if these providers create SQL queries using untrusted input from URIs without adequate validation or parameterization, they risk becoming...
- MASTG-TEST-0376 — References to Native Bridge APIs in WebViews: iOS apps can establish a bidirectional communication channel between JavaScript and native code through WebView-native bridges. When using `WKWebView`, message handlers are registered on the `WKUserContentController` via `add(_:name:)`)...
- MASTG-TEST-0377 — References to `evaluateJavaScript` Used as Bridge Reply in `WKScriptMessageHandler`: When a `WKScriptMessageHandler` receives a message from JavaScript and needs to return data, a common pattern is to call `evaluateJavaScript:completionHandler:`) to invoke a JavaScript callback such as `window.receiveData(...)`.
- MASTG-TEST-0379 — References to `evaluateJavaScript` Without Content World Isolation: When an app uses `evaluateJavaScript(_:completionHandler:)`) to read data from the DOM (for example, to extract form field values, account details, or page structure), the script executes in the `.page` world. In this world, the...
- MASTG-TEST-0380 — References to `evaluateJavaScript` Writing Sensitive Data into WebView DOM: When a `WKWebView` app needs to display sensitive information (such as a one-time password, account balance, or payment detail), a common pattern is to inject that data directly into the DOM using...

Mapped MASTG best practices:

- MASTG-BEST-0011 — Securely Load File Content in a WebView: The recommended approach to **load file content to a WebView securely** is to use `WebViewClient` with `WebViewAssetLoader` to load assets from the app's assets or resources directory using `https://` URLs instead of insecure `file://`...
- MASTG-BEST-0012 — Disable JavaScript in WebViews: Enabling JavaScript is **not a vulnerability by itself**. In real apps it is often required for legitimate functionality, such as rendering modern web applications, interactive account portals, support centers, payment or login flows,...
- MASTG-BEST-0013 — Disable Content Provider Access in WebViews: Unlike other file content access methods from `WebSettings`, the `setAllowContentAccess` method always defaults to `true`. Therefore, **whenever access to content providers isn't explicitly needed**, ensure that the...
- MASTG-BEST-0035 — Prefer Origin Scoped Messaging Over Legacy JavaScript Bridges: JavaScript bridges are not inherently unsafe, but they are a high-impact `WebView` feature and should only be exposed to content you fully trust. The main risk is not the bridge alone, but the combination of a bridge with untrusted or...
- MASTG-BEST-0039 — Prevent SQL Injection in ContentProviders: The `ContentProvider` enables Android applications to share data with other applications and system components. If a `ContentProvider` constructs SQL queries using untrusted input from URIs, IPC calls, or Intents without validation or...
- MASTG-BEST-0058 — Restrict Native Functionality Exposed Through WebView Bridges: When using `WKWebView`, native functionality can be exposed to JavaScript through message handlers registered via `WKUserContentController.add(_:name:)`). Any JavaScript running in the WebView can call...
- MASTG-BEST-0062 — Use WKScriptMessageHandlerWithReply to Return Data to JavaScript: When a native bridge handler needs to return data to JavaScript, the common pattern of calling `evaluateJavaScript:completionHandler:`) with a callback string such as `window.receiveData(...)` injects the return value into the page's...
- MASTG-BEST-0061 — Use WKContentWorld Isolation for DOM Inspection Scripts: When an app uses `evaluateJavaScript(_:completionHandler:)`) or `WKUserScript` to read data from the DOM (for example, to extract form field values, account details, or page metadata), that code runs in the `.page` world by default. In...
- MASTG-BEST-0059 — Render Sensitive UI as Native Views Over the WebView: When a `WKWebView` needs to present sensitive UI, such as a credential picker, autofill suggestion, or payment confirmation, rendering that interface as HTML elements inside the WebView exposes it to any JavaScript running on the page....

Mapped MASTG knowledge:

- MASTG-KNOW-0018 — WebViews: On Android versions prior to 4.4, WebViews used the WebKit rendering engine to display web pages. Since Android 4.4, WebViews have been based on Chromium, providing improved performance and compatibility. However, the pages are still...
- MASTG-KNOW-0117 — Android ContentProvider: A `ContentProvider` is an Android component that exposes structured data to other apps and system services through a standardized URI-based interface. Providers support CRUD operations (`query`, `insert`, `update`, `delete`) and are...
- MASTG-KNOW-0076 — WebViews: WebViews are in-app browser components for displaying interactive web content. They can be used to embed web content directly into an app's user interface. iOS WebViews execute JavaScript and render HTML, and therefore can execute...
- MASTG-KNOW-0139 — WKContentWorld: `WKContentWorld`, introduced in iOS 14, represents an isolated JavaScript execution environment within a `WKWebView`. Each content world has its own JavaScript global scope and its own copy of the built-in prototype chain, but all...
