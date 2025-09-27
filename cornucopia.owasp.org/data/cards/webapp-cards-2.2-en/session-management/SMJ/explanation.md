## Scenario: Jeff’s Replay Attack Exploitation

Consider a scenario where Jeff exploits a system vulnerability that allows for the acceptance of repeated identical interactions, such as HTTP requests, signals, or button presses. This issue arises because:

1. **Lack of Replay Attack Protection:** The system does not have mechanisms to detect and reject duplicate submissions of the same action.

### Example

Jeff observes an online transaction process where a user submits a payment form. He captures the HTTP request of this transaction and later resends the exact same request multiple times. The system, lacking checks for duplicate requests, processes each one as a valid transaction. As a result, the same payment is made multiple times, leading to financial loss or discrepancies in accounting.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

**Tampering** involves unauthorized modification of data or messages, including altering, injecting, or replaying them.
Jeff resends an identical request (a replay attack) and the system accepts it as new, effectively modifying the state of the system (e.g., triggering multiple transactions).
The attack is not about impersonation (Spoofing) per se, but about unauthorized manipulation of data/state, which is classic **Tampering**.

### What can go Wrong?

Such vulnerabilities can lead to replay attacks, resulting in unauthorized transactions, data breaches, and exploitation of system functionalities.

### What are you going to do about it?

1. Implement measures to detect and reject duplicate requests, such as tracking and validating unique tokens for each interaction.
2. Ensure that critical actions like transactions, state changes, or command submissions are safeguarded against repeat submissions.
3. Regularly audit and update security protocols to address and prevent replay attacks.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
