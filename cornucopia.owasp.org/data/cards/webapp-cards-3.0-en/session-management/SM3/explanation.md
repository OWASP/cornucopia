## Scenario: Ryan’s Exploitation of a Poorly Implemented Sessions Magement System

Imagine a scenario where Ryan takes advantage of a system that doesn't sufficiently give the user the overview of their active sessions, and allows multiple concurrent sessions without proper controls. He exploits the following vulnerabilities:

1. **Allowance of Multiple Active Sessions:** The system does not give the user an overview over which devices that are logged in. This allowes Ryan to log in on a device while the legitimate user is also active, without the user being aware of it.
2. **Lack of Controls on Concurrent Sessions:** The system fails to restrict or monitor concurrent sessions, enabling Ryan to access the account without detection.
3. **No Alerts for Unusual Concurrent Access:** The system does not alert users or administrators about unusual patterns of concurrent access, such as logins from other countries or old devices.
4. **Inadequate Session Management Policies:** The system does not have robust session management policies to handle scenarios like authorization code theft or session fixation. If a session gets compromised, Ryan can continue to use it without the system detecting the breach or being able to empower administrators and users to take appropriate actions.

### Example

Ryan discovers that someone at the airport has left their mobile device unattended. He steals the device and takes it home. He then finds out that the user still has an active session on the device, and uses it to access the account. The user is unaware of this access, and the system does not have any controls or alerts in place to detect or prevent it. Ryan can then access sensitive information and perform unauthorized actions without being detected.

## Threat Modeling

### STRIDE

This scenario falls under STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user or system.
Ryan exploits a poorly implemented session management system that allows him to access active sessions without the user's knowledge or being able to prevent it.

### What can go wrong?

Poorly implemented session management can lead to unauthorized access and exploitation of user accounts, potentially compromising data security and privacy.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are we going to do about it?

For many applications it may be desirable to allow customers to be logged in using multiple browsers/devices. Consider implementing a policy to restrict or carefully monitor concurrent sessions. Options include implementing impossible travel detection, alerting in case of logins from geographically distant locations within a short timeframe, or even from old devices. Require the use of MFA, in these cases. Also consider that users should be informed about active sessions and be able to manage them, including terminating sessions that they do not recognize. This can help mitigate the risk of unauthorized access and provide users with greater control over their accounts. Additionally, implementing robust session management policies can help detect and prevent session fixation and authorization code theft, further enhancing the security of the application.

1. Implement a policy to restrict or carefully monitor concurrent sessions.
2. Require the use of MFA for logins from new devices or locations.
3. Provide users with an overview of their active sessions and the ability to manage them, including terminating sessions that they do not recognize.
4. Implement robust session management policies to detect and prevent session fixation and authorization code theft.
5. Regularly review and update session management policies to ensure they effectively protect against unauthorized access and account compromise.
6. Educate users about the importance of monitoring their active sessions and recognizing signs of unauthorized access.
7. Implement alerts for unusual concurrent access patterns, such as logins from other countries or old devices, to enhance security and enable timely responses to potential breaches.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
