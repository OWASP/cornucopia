## Scenario: Piotr's Clickjacking Attack

Piotr embeds the target application in a transparent or disguised frame on his own site, tricking authenticated users into clicking interface elements that perform sensitive actions they never intended to take. This occurs because:

1. **No frame embedding restrictions:** The application does not set `X-Frame-Options` or a `frame-ancestors` Content Security Policy directive, allowing any site to embed it in an `<iframe>`.

2. **Sensitive actions reachable by a single click:** Critical functions — such as confirming a transfer, deleting an account, or granting permissions — can be triggered in one interaction, making them vulnerable to UI redress attacks.

### Example

Piotr creates a page offering a free prize draw. The page contains a "Click to claim your prize!" button styled to appear prominently. Behind it, positioned precisely over the button using CSS, is an invisible iframe embedding a banking application's "Confirm Transfer" page, pre-loaded with Piotr's account as the destination. When an authenticated banking customer clicks what they believe is the prize button, they actually click the bank's confirm button inside the hidden frame. The bank processes the transfer with the victim's session — no credentials were stolen and nothing appears unusual in the bank's logs.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Piotr manipulates the user's interaction with the application, causing the victim to perform an action they did not intend. The user's own authenticated session is weaponized against them. 

### What can go wrong?

Clickjacking turns any one-click sensitive operation into an attacker-controllable action requiring only that the victim visit a malicious page while authenticated. Operations commonly exploited include fund transfers, password changes, permission grants, account deletions, and social media posts. Because the victim genuinely performs the action through their own session, the request appears entirely legitimate to the server.

### What are we going to do about it?

Prevent the application from being embedded in frames controlled by untrusted origins.

1. Set the `Content-Security-Policy: frame-ancestors 'none'` directive (or `frame-ancestors 'self'` if legitimate embedding is needed) on all application responses; this is the modern, preferred approach.
2. Supplement with the `X-Frame-Options: DENY` (or `SAMEORIGIN`) header for compatibility with older browsers that do not support CSP `frame-ancestors`.
3. For sensitive one-step actions, require user confirmation through an interaction that cannot be pre-positioned — such as entering a value, solving a challenge, or re-authenticating before the action completes.
4. Implement CSRF tokens on state-changing requests so that even if a click is captured, the request cannot be submitted without the valid token generated for the victim's session.
5. Test for clickjacking by attempting to embed the application in an iframe on an external domain and verifying that the browser blocks the frame.
