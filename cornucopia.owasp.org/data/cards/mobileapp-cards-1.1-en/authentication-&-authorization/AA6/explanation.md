## Scenario: Anant can perform sensitive operations without additional authentication because authentication requirements are too weak or missing

Consider Anant, an adventurous user who believes that logging in once should grant him eternal, unquestioned power. He thinks, "I'm already in the house; why do I need a key for the bathroom?" If the app fails to ask for re-authentication during critical moments, Anant will happily perform high-stakes operations—like transferring funds or deleting accounts—without a second glance.

### Example

Anant is using the "CryptoEx" trading app. He logs in with his fingerprint. He navigates to the "Withdraw All Funds" screen. The app usually asks for a transaction PIN. However, Anant notices that the PIN check is only performed by the Javascript on his phone. He uses a proxy tool to capture the "Withdraw" API request and replays it, stripped of any PIN validation usage. The server, assuming the client app did its job, processes the withdrawal. Anant clears out the account while the PIN screen is still waiting for input.

## Threat Modeling

### STRIDE

This scenario falls under the **Spoofing** and **Elevation of Privilege** categories of STRIDE.

By skipping the re-authentication step, Anant is **Spoofing** a user with verified intent, leading to **Elevation of Privilege** by performing sensitive actions without the required authorization.

### What can go wrong?

**Critical Actions Without Verification:** Attackers with temporary access (e.g., unlocked phone) can perform irreversible actions.

**Bypassed Security Controls:** Client-side checks for PINs or passwords can be skipped entirely.

### What are we going to do about it?

**Server-Side Validation:** Distinct sensitive operations should require a fresh session token or validation from the server, not just a "flag" in the app.

**Step-Up Authentication:** Enforce re-authentication (password, biometric, 2FA) for sensitive actions on the server.

**Freshness Checks:** Ensure the session or token used for the action is "fresh" (e.g., authenticated within the last 5 minutes).


https://mas.owasp.org/MASWE/MASVS-AUTH/MASWE-0029/