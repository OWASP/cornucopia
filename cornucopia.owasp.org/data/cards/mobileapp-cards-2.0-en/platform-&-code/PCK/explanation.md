## Scenario: Grant can modify or expose data by influencing or altering JavaScript bridges, extensions, or interprocess communication such as shared memory, message passing, pipes, or sockets

Consider a scenario where Grant has identified the target app exposes a `@JavascriptInterface`-annotated class with methods including `getSessionToken()` and `writePreference(key, value)`. He delivers a crafted HTML page to the app's WebView via an unvalidated deep link. The page calls `window.NativeBridge.getSessionToken()` and `window.NativeBridge.writePreference("admin", "true")`. Grant now has the session token and has promoted himself to admin. The JavaScript bridge was originally added for legacy web compatibility and never removed.

1. JavaScript bridges give arbitrary web-page JavaScript direct access to native device APIs.
2. `postMessage`-based communication without origin validation relays attacker-controlled content into native handlers.
3. Shared memory, pipes, or sockets between app processes without integrity checks allow one process to feed malicious data to another.

### Example

Grant discovers the app's inter-process notification service accepts URLs via a Binder interface and loads them in an internal WebView. He sends a `javascript:` URL through the Binder interface. The WebView executes the script. Grant now has access to every native method on the bridge. The service was designed for displaying HTML notifications. It was not designed for untrusted callers. The distinction was never implemented.

## Threat Modeling

### STRIDE

This scenario falls under **Tampering** and **Elevation of Privilege**.

A JavaScript bridge grants untrusted JavaScript — arriving via an attacker-controlled URL or injected script — direct access to native capabilities, effectively bypassing the sandboxing that separates web and native execution contexts.

### What can go wrong?

- Native methods (file access, credential retrieval, preference modification) are exposed to any JavaScript running in the WebView.
- Shared-memory IPC without integrity verification allows one process to feed malicious data to another.
- `postMessage` handlers without origin checks accept messages from attacker-controlled iframes or pages.

### What are we going to do about it?

- Remove `addJavascriptInterface` from production builds unless absolutely required; if kept, expose only a minimal interface and validate every input.
- Restrict JavaScript execution to allowlisted origins within the WebView.
- Validate the `origin` of every `postMessage` before processing the message.
- For inter-process pipes or shared memory: authenticate peers and verify message integrity with a MAC.
