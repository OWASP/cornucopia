## Scenario: Elena's Malicious Browser Extension Attack

Elena uses a malicious or over-privileged browser extension installed on the victim's machine to read the application's DOM, steal authentication tokens, and invoke internal frontend APIs — all without any vulnerability in the application itself. This occurs because:

1. **Broad extension permissions:** The extension was granted host permissions to read and modify page content on all websites, giving it unrestricted access to any page the user visits.

2. **Sensitive data in the DOM and storage:** Authentication tokens, session cookies (where readable by JavaScript), user data, and internal API endpoints are accessible in the page's JavaScript context, which extensions can inspect and modify.

3. **No isolation between extension and page context:** Content scripts injected by extensions share access to the DOM and can observe network requests, keyboard events, and page state, providing a complete view of the user's interaction with the application.

### Example

Elena publishes a browser extension marketed as a productivity tool that helps users manage browser tabs. The extension requests access to read and change data on all websites. Once installed, it silently monitors every page the user visits. When the user logs into their company's HR portal, Elena's extension reads the JWT from `localStorage`, captures the values entered into salary update forms before they are submitted, and exfiltrates both to Elena's server. Because the extension runs in the browser with the user's own permissions, it appears as normal local processing and generates no anomalous server-side traffic.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

Elena's extension reads data that the user and application treat as private — tokens, form inputs, and rendered page content — without any server-side interaction that could be detected or blocked. A secondary category of **Tampering** applies if the extension modifies requests or page content; **Elevation of Privilege** applies if the stolen tokens are reused to impersonate the victim.

### What can go wrong?

A malicious extension with broad permissions is effectively a keylogger and DOM scraper running at the browser level, with access to every authenticated session the user has open. Stolen tokens can be used to take over accounts, scraped form data can expose credentials and sensitive business information, and injected scripts can silently alter transactions before they are submitted to the server.

### What are we going to do about it?

Reduce the application's exposure to extension-level access and educate users about extension risk.

1. Store authentication tokens in `HttpOnly` cookies so they are inaccessible to JavaScript — and therefore inaccessible to extension content scripts — rather than in `localStorage` or `sessionStorage`.
2. Apply a strict Content Security Policy to limit what scripts can execute on the page, reducing extension injection vectors even if a script is injected.
3. Where the organization controls the browser environment (e.g., enterprise deployments), enforce an allowlist of approved extensions through device management policy.
