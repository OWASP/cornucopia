## Platform-Aware Review Guidance

**Server-Side**
- Implement a server-side session state machine for multi-step flows: each API endpoint checks the session state before processing, not just the step parameter.
- Return step-completion tokens (short-lived JWTs or opaque tokens) that the next step must present; the server validates the token, not a client-supplied flag.
- Use server-authoritative timestamps for all token expiry; reject tokens where `iat` or `exp` differs from server time by more than an acceptable skew (e.g., 5 minutes).

**Android**
- Do not store multi-step flow progress in `SharedPreferences` or `Intent` extras; store it only in server-side session state.
- Verify that the app does not allow deep-linking directly into the middle of an authentication flow without a server-verified step token.

**iOS**
- Avoid `UserDefaults` for any value that represents authentication state; it is not protected and can be modified on jailbroken devices.
- Validate all completion tokens server-side via a signed challenge-response, not by checking a local boolean.

**Testing**
- Replay step N+1's network request directly after completing step 1, skipping all intermediate steps; verify the server rejects it.
- Set the device clock 24 hours in the past and attempt to use an expired token; verify the server rejects it.
- Intercept the multi-step flow with a proxy (Burp Suite / mitmproxy) and tamper with step-tracking parameters.

**OWASP Mappings**
- MASVS: AUTH-1, AUTH-3
- MASTG: TEST-0034, TEST-0079
- MASWE: MASWE-0030
