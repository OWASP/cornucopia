## Scenario: John’s Prediction of Session Identifiers

Imagine a scenario where John exploits weaknesses in session management by predicting or guessing session identifiers. He capitalizes on several system vulnerabilities:

1. **Static Identifiers Across Role Changes:** Session IDs remain unchanged when a user’s role alters, such as pre and post-authentication.

2. **Unchanged IDs Across Communication Modes:** Identifiers do not change when switching between non-encrypted and encrypted communications.

3. **Insufficient Length and Randomness:** Session identifiers are not sufficiently long or randomly generated.

4. **Lack of Periodic ID Refresh:** The system does not periodically change session identifiers.

### Example

John targets an e-commerce website where users’ session IDs remain the same before and after they log in. By predicting the session ID pattern used when users are browsing without logging in, John guesses the IDs post-login. This allows him to hijack sessions where users are authenticated and potentially access sensitive information or make unauthorized purchases.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** involves impersonating a legitimate user.
John predicts or guesses session identifiers because the system does not rotate or randomize them appropriately.
By hijacking a valid session ID, he assumes the identity of the authenticated user, which is classic **Spoofing**.

### What can go Wrong?

Such practices expose users to session hijacking and potential privacy breaches, as attackers can easily predict or guess session IDs.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

1. Implement a system to regenerate session IDs upon any change in user state, especially during authentication processes.
2. Ensure session IDs are sufficiently long, complex, and randomly generated.
3. Regularly refresh session identifiers to prevent them from being guessed or reused over time.
4. Employ strict security measures for session management across both encrypted and non-encrypted communications.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
