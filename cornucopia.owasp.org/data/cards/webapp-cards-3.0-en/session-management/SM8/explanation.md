## Scenario: Matt’s Abuse of Long-Lasting Sessions

Visualize a scenario where Matt exploits the lack of periodic re-authentication in an application. This issue arises because:

1. **Prolonged Session Duration:** The application allows sessions to remain active for extended periods without re-verifying the user's identity or privileges.

2. **No Checks for Privilege Changes:** The system does not reassess user privileges during long sessions, potentially missing changes in user status or permissions.

3. **Inadequate protection against session hijacking:** If a session is compromised, the attacker can maintain access for a long time without being detected due to the absence of periodic re-authentication, or other controls like geolocation checks, enforced client fingerprinting, or anomaly detection.

### Example

Matt gains access to an employee’s account after stealing an unlocked computer at a train station early in the morning. Later that day, the employee’s access rights gets revoked after the employee notifies the IT department. However, since the system does not require re-authentication, check for privilege changes during active sessions, or implement other controls like geolocation checks, enforced client fingerprinting, or anomaly detection, Matt can continue to have access to sensitive information and system functionalities all day, exploiting the unchanged session privileges.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user.
Matt exploits the lack of periodic re-authentication to maintain access to the system, effectively impersonating the legitimate user without needing to re-enter credentials. The core issue is unauthorized impersonation through an active session, making **Spoofing** the correct primary category. Other STRIDE categories like **Privilege Escalation** may be relevant in certain contexts where the revocation of privileges isn't immediately enforced.

### What can go wrong?

This vulnerability can lead to unauthorized access and misuse of privileges, especially in cases where user privileges have been altered or revoked.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

1. Implement a system for periodic re-authentication, especially for sessions that last beyond a certain time threshold.
2. Regularly check and update user privileges within active sessions to ensure they reflect current permissions.
3. Consider introducing shorter session timeouts for highly sensitive applications, requiring users to re-authenticate more frequently.
4. Implement additional controls such as geolocation checks, enforced client fingerprinting, or anomaly detection to identify and mitigate potential session hijacking.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
