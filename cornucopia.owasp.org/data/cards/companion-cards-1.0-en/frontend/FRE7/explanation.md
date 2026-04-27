### Scenario: Carlos Reads and Manipulates Sensitive Data via Misconfigured CORS and Unsafe postMessage

Carlos reads or manipulates sensitive data from an application's frontend by exploiting a misconfigured CORS policy or unsafe `postMessage` handling, allowing his malicious origin to access data it should never be able to reach. This occurs because:

1. **Overly permissive CORS policy:** The server responds with `Access-Control-Allow-Origin: *` or echoes the requesting origin without validation, permitting any site to make credentialed cross-origin requests and read the responses.

2. **Unsafe postMessage handling:** The application receives messages via `window.postMessage` without verifying the sender's origin, trusting any embedded frame or window to pass it data or commands.

3. **Sensitive data in client-accessible contexts:** Authenticated API responses, embedded iframes, or cross-window communication expose data that Carlos's malicious page can read once the origin restriction is removed or bypassed.

### Example

A financial dashboard allows partner sites to embed it in an iframe and communicate via `postMessage`. The message listener in the application checks for a specific action name but does not validate `event.origin`. Carlos hosts a page on a domain he controls, embeds the dashboard in a hidden iframe, and sends a `postMessage` with the expected action name. The application responds with the authenticated user's account balance and recent transactions, which Carlos's outer page reads and exfiltrates. He distributes a phishing link pointing to his page and collects financial data from every victim who clicks it while logged into the dashboard.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Carlos exploits misconfigured CORS and unsafe `postMessage` handling to manipulate sensitive data and trigger unauthorized state changes. By bypassing origin restrictions, he can not only read authenticated responses but also send crafted messages that cause the application to perform unintended actions—such as modifying account settings, transferring funds, or executing transactions—on behalf of the victim. The lack of origin validation transfers trust to any attacker-controlled origin, enabling him to tamper with both data integrity and application behavior.

### What can go wrong?

A permissive CORS policy on an authenticated API turns any attacker-controlled website into a proxy for that API, with the victim's credentials silently attached. Unsafe `postMessage` handling can expose private data, trigger state-changing actions, or serve as a pivot for further attacks such as session hijacking. The victim is typically unaware that anything has occurred.

### What are we going to do about it?

Apply strict origin validation to all cross-origin communication channels.

1. Set CORS headers to allow only explicitly listed, trusted origins; never echo the `Origin` header back without validation, and never use `Access-Control-Allow-Origin: *` on endpoints that return sensitive data.
2. Avoid `Access-Control-Allow-Credentials: true` unless absolutely necessary and combined with an explicit, validated allowlist of origins.
3. In every `postMessage` listener, validate `event.origin` against a strict allowlist before processing the message or acting on its content.
4. Audit all iframe embedding: use the `X-Frame-Options` or `frame-ancestors` CSP directive to control which origins may embed the application.