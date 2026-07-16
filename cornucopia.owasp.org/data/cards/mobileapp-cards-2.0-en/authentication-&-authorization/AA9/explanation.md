## Scenario: Wong can bypass the authentication because it does not fail securely — it defaults to allowing unauthenticated access

Consider a scenario where Wong discovers that if the biometric hardware returns an error (sensor unavailable, too many failed attempts, or a thrown exception from the biometric API), the app's authentication flow catches the exception and falls through to a code path that sets `authState = AUTHENTICATED`. The authentication fails open: an error is treated as success.

1. Exceptions from the biometric or authentication API are caught without a secure fallback, and execution continues as if authentication succeeded.
2. A boolean `authenticated` flag is initialized to `true` and only set to `false` on explicit failure — meaning any exception or early return leaves it `true`.
3. Network-dependent authentication: if the server is unreachable, the app allows offline access rather than denying it.

### Example

Wong triggers a temporary hardware sensor error (by covering the fingerprint sensor and submitting multiple deliberate failures). The app's `authenticate()` function throws `AuthenticationException`. The catch block logs the exception and calls `proceed()`, which was the next line in the original non-exception flow. The authentication state is never explicitly set to "failed." The app opens. Wong is now authenticated as the device owner without presenting any valid credential. The developer's intention was graceful degradation. The result was an open door.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing**.

Wong impersonates an authenticated user by exploiting a fail-open authentication implementation. Any condition — hardware error, network timeout, exception — that causes the authentication check to be skipped results in unauthorised access.

### What can go wrong?

- Authentication errors or exceptions result in unauthenticated access to sensitive data.
- Network-unreachable errors during remote authentication allow offline access that the policy intended to deny.
- Race conditions between authentication state transitions result in a briefly unauthenticated window.

### What are we going to do about it?

- Initialise all authentication state to "not authenticated" (fail-closed); only set it to "authenticated" on explicit, verifiable success.
- In all exception handlers and fallback paths, set authentication state to "failed" and navigate to the login screen.
- For cryptographic authentication: rely on the success of the cryptographic operation, not a boolean flag; if the decryption fails (e.g., key not unlocked), the data is not available — no flag manipulation can change this.
- For remote authentication: if the server is unreachable and online authentication is required by policy, deny access rather than fall back to an offline mode that was not explicitly designed and reviewed.
