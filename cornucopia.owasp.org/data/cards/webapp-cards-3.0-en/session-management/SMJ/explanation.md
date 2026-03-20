## Scenario: Jeff’s Replay Attack Exploitation

Jeff can reuse stolen session identifiers and/or tokens because they are not handled confidentially or because there is no strong proof of possession (e.g. binding to certificate, device, IP address, user-agent, etc.)

Consider a scenario where Jeff exploits a system vulnerability that allows him to reuse stolen session identifiers or tokens without any checks for their validity or proof of possession. This issue arises because the system does not have mechanisms to detect and reject forged or replayed session identifiers or tokens, allowing attackers to reuse them for unauthorized access or actions.

1. **Lack of Confidential Handling:** Session identifiers or tokens are not treated as sensitive information, leading to their exposure and potential theft.
2. **Absence of Proof of Possession:** The system does not require any form of proof that the session identifier or token is being used by the legitimate owner, such as binding it to a specific device, IP address, user-agent, or using cryptographic methods.
3. **No Detection of Reuse:** The system does not have mechanisms to detect and reject replayed session identifiers or tokens, allowing attackers to reuse them for unauthorized access or actions.

### Example

Jeff observes an online transaction process where a user submits a payment form. He captures the HTTP request of this transaction and later resends the exact same request multiple times. The system, lacking checks for proof of possession and replay detection, processes each request as if it were a valid transaction, allowing Jeff to execute multiple unauthorized transactions using the same session identifier or token.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Tampering**.

**Tampering** involves unauthorized modification of data or messages, including altering, injecting, or replaying them.
Jeff resends an identical request (a replay attack) and the system accepts it as new, effectively modifying the state of the system (e.g., triggering multiple transactions).
The attack is not about impersonation (Spoofing) per se, but about unauthorized manipulation of data/state, which is classic **Tampering**.

### What can go wrong?

Such vulnerabilities can lead to replay attacks, resulting in unauthorized transactions, data breaches, and exploitation of system functionalities.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Treat session identifiers and tokens as sensitive information, ensuring they are handled confidentially and securely.
2. Implement proof of possession mechanisms, such as binding session identifiers or tokens to specific devices, IP addresses, user-agents, or using cryptographic methods to ensure that they can only be used by the legitimate owner.
3. Implement mechanisms to detect and reject replayed session identifiers or tokens, such as using nonces, timestamps, or maintaining a list of recently used identifiers/tokens to prevent their reuse.
4. Consider implementing additional security measures such as multi-factor authentication, anomaly detection, and rate limiting to further protect against replay attacks.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
