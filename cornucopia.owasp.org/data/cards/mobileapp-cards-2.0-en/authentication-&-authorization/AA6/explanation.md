## Scenario: Anant can perform sensitive operations without step-up or repeated authentication because authentication requirements do not respond to transaction risk or contextual changes

Consider a scenario where Anant has physical access to a device that was unlocked by the owner 10 minutes ago. The owner stepped away. The banking app's session is still active. Anant initiates a fund transfer to an external account. The app does not require re-authentication for transfers, because the session is valid. Anant transfers a significant amount. The session was "trusted" because the user authenticated at app launch — a contextual state that had since changed materially.

1. A session established at app launch may remain fully trusted even when the device is unattended.
2. High-risk operations (large transfers, account changes, data exports) do not require proportional authentication challenges.
3. Context changes — app moving from background to foreground, network change, location change — do not trigger re-evaluation of trust.

### Example

Anant borrows a colleague's phone for "a moment." The colleague's banking app is in the background. Anant brings it to the foreground and initiates a transfer. The app's last authentication was 8 minutes ago. The session timeout is 15 minutes. No biometric prompt appears for the transfer. The transfer completes. The colleague discovers the loss at end-of-day. The app's UX team had deliberately removed step-up authentication to "reduce friction." Friction sometimes serves a purpose.

## Threat Modeling

### STRIDE

This scenario falls under **Spoofing** and **Elevation of Privilege**.

Without step-up authentication, Anant can act with the full privileges of the authenticated user for any operation, regardless of the risk level of that operation.

### What can go wrong?

- High-value transactions are completed by an attacker who has brief physical access to an unlocked device.
- A stolen session token allows unlimited operations without any additional authentication challenge.
- Contextual trust signals (device lock, network change, inactivity timeout) are ignored, leaving sessions perpetually trusted.

### What are we going to do about it?

- Implement risk-adaptive authentication: require step-up (biometric prompt or remote challenge) for operations above a defined risk threshold (large amount, new payee, account change).
- Enforce an inactivity timeout: re-authenticate after a period of inactivity, especially for sensitive screens.
- Re-authenticate when the app transitions from background to foreground after a significant interval.
- Bind the step-up authentication to the specific operation via a server-issued challenge, so that a replayed authentication cannot be used for a different transaction.
