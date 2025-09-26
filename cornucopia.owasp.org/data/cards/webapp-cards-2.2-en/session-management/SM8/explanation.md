## Scenario: Matt’s Abuse of Long-Lasting Sessions

Visualize a scenario where Matt exploits the lack of periodic re-authentication in an application. This issue arises because:

1. **Prolonged Session Duration:** The application allows sessions to remain active for extended periods without re-verifying the user's identity or privileges.

2. **No Checks for Privilege Changes:** The system does not reassess user privileges during long sessions, potentially missing changes in user status or permissions.

### Example

Matt gains access to an employee’s account in a corporate system early in the day. Throughout the day, the employee’s access rights are revoked due to a change in their employment status. However, since the system does not require re-authentication or check for privilege changes during active sessions, Matt continues to have access to sensitive information and system functionalities all day, exploiting the unchanged session privileges.

## Threat Modeling

### STRIDE

This scenario maps primarily to STRIDE: **Elevation of Privilege**.

**Elevation of Privilege** (EoP) occurs when an attacker gains access to more privileges than they are supposed to have.
In this case, Matt exploits long sessions without periodic re-authentication. Even though the legitimate user’s privileges are reduced during the day, the session retains the previous access rights.
The attack is not about impersonating someone new (Spoofing), but about continuing to have unauthorized privileges, which is classic **Elevation of Privilege**.

### What can go Wrong?

This vulnerability can lead to unauthorized access and misuse of privileges, especially in cases where user privileges have been altered or revoked.

### What are you going to do about it?

1. Implement a system for periodic re-authentication, especially for sessions that last beyond a certain time threshold.
2. Regularly check and update user privileges within active sessions to ensure they reflect current permissions.
3. Consider introducing shorter session timeouts for highly sensitive applications, requiring users to re-authenticate more frequently.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
