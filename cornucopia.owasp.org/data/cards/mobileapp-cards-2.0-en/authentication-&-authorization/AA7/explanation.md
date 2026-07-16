## Scenario: Abdullah can bypass authentication by altering the usual process sequence or flow, by undertaking the process in incorrect order, by manipulating date and time values used by the app, or by using valid features for unintended purposes

Consider a scenario where Abdullah is probing a multi-step account-recovery flow. The flow is: step 1 — enter username; step 2 — answer security questions; step 3 — set new password; step 4 — confirmation. Abdullah skips step 2 by directly posting to step 3's endpoint. The server does not verify that step 2 was completed. Abdullah sets a new password for the account. He did not need to know the answers to the security questions; he needed to know the step order was not enforced.

1. Multi-step flows that do not server-side validate completion of prior steps are vulnerable to step-skipping.
2. Date and time manipulation (setting the device clock to the past) can bypass time-based token expiry or subscription checks.
3. Valid features used for unintended purposes: a "remember me" token meant for a 30-day login being reused indefinitely because no server-side expiry is enforced.

### Example

Abdullah finds the app stores a `step_completed` flag in `SharedPreferences` to track which authentication step is current. He modifies the flag to indicate step 2 is already done and navigates directly to step 3. The client-side state is trusted by the server. The server does not maintain its own session-state machine. Abdullah resets the account password without completing the identity verification step. The "multi-factor" account recovery turned out to be single-factor for attackers who could edit local storage.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

By bypassing or reordering authentication steps, Abdullah gains privileges he has not legitimately earned, impersonating a properly authenticated user.

### What can go wrong?

- Account takeover via password reset without identity verification.
- Session tokens granted before all required authentication factors are satisfied.
- Time-based token expiry bypassed by device clock manipulation.
- Business logic enforced client-side only can be skipped by an attacker who modifies local state.

### What are we going to do about it?

- Maintain all multi-step flow state server-side; the server must track which steps have been completed and reject requests for a later step if earlier steps are not verified.
- Never trust client-side state (SharedPreferences, local flags, URL parameters) as proof that a step was completed.
- Use server-generated, signed step-completion tokens; each step returns a signed assertion that the next step can verify server-side.
- Validate date/time sensitive tokens against server time, not device time; reject tokens with excessive clock skew.
- Apply least-privilege: grant only the capabilities appropriate to the authentication level achieved so far, not the final level.
