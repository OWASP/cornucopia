## Scenario: Olga's Token Theft and Session Hijacking

Olga uses malicious JavaScript running in the victim's browser to steal authentication tokens and then uses them to take over the user's session, gaining full access to the account without knowing the user's password. This occurs because:

1. **Tokens accessible to JavaScript:** Authentication tokens — session cookies without the `HttpOnly` flag, JWTs stored in `localStorage`, or access tokens held in JavaScript variables — can be read by any script executing in the page's origin.

2. **Execution vector available:** Olga can run JavaScript in the victim's browser through a cross-site scripting vulnerability, a compromised third-party script, or a malicious browser extension.

### Example

A project management application stores its JWT access token in `localStorage` after login. Olga discovers a stored XSS vulnerability in the comments section of a shared project. She posts a comment containing a script that reads `localStorage.getItem('token')` and sends the value to a server she controls. When a project administrator views the comments page, the script executes silently in their browser, exfiltrating their JWT. Olga imports the token into her own browser using a developer console and makes authenticated API calls as the administrator — resetting passwords, exporting data, and inviting her own accounts as collaborators.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Spoofing**.

Olga presents a stolen token to the backend and is indistinguishable from the legitimate user. She does not break the authentication mechanism itself — she steals a valid credential and reuses it from a different context.

### What can go wrong?

Session hijacking gives an attacker complete control over the victim's account for as long as the token remains valid. All actions taken through the hijacked session are attributed to the victim in audit logs, complicating incident response. Depending on the application, this can lead to data exfiltration, financial fraud, account takeover, or lateral movement to other systems the victim has access to.

### What are we going to do about it?

Protect authentication tokens from JavaScript access and limit the window of opportunity for stolen tokens to be reused.

1. Set the `HttpOnly` flag on session cookies so that JavaScript cannot read them; use cookies for authentication tokens rather than `localStorage` wherever possible.
2. Set the `Secure` flag on authentication cookies so they are only transmitted over HTTPS, and apply the `SameSite=Strict` or `SameSite=Lax` attribute to reduce cross-site request risks.
3. Keep token lifetimes short and implement refresh token rotation, so a stolen access token expires quickly.
4. Eliminate XSS vulnerabilities that would give an attacker a JavaScript execution vector — address the root cause, not only the token storage mechanism.