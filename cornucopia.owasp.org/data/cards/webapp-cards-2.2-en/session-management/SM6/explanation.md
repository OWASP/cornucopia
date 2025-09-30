## Scenario: Gary’s Session Takeover Tactics

Picture a scenario where Gary exploits session management weaknesses to take over a user's session. He takes advantage of:

1. **Long or No Inactivity Timeout:** Sessions remain active despite prolonged user inactivity.

2. **Extended or No Overall Session Time Limit:** Sessions do not have a defined expiration time.

3. **Multi-Location Session Usage:** The system allows the same session to be used simultaneously from different devices or locations.

### Example

Gary identifies that an online banking platform does not enforce inactivity timeouts. A user logs into their account but forgets to log out. The session remains active indefinitely, giving Gary an opportunity to access this session if the user’s device is left unattended or compromised. Additionally, the system’s allowance of the same session being used from multiple locations enables Gary to maintain access even when the legitimate user is active elsewhere.

## Threat Modeling

### STRIDE

This scenario falls under STRIDE: **Spoofing**.
**Spoofing** is about impersonating a legitimate user or system.
Gary exploits long or missing inactivity/overall session timeouts and the ability to use the same session from multiple locations.
By taking over an active session, he effectively assumes the identity of the legitimate user, which is classic Spoofing.

### What can go wrong?

This vulnerability can lead to unauthorized session takeovers, leading to potential data theft, financial loss, and privacy breaches.

For more things that can go wrong, see the [Common Attack Patterns related to this card](#mapping 'Common Attack Patterns related to this card [internal]') in the table below.

### What are you going to do about it?

There should be a session inactivity timeout that is as short as possible, based on balancing risk and business functional requirements. This could be role-dependent. Additionally disallow persistent logins and enforce periodic session terminations (e.g. after 8 or 12 hours), even when the session is active, especially for applications supporting rich network connections or connecting to critical systems. Termination times should support business requirements and the user should receive sufficient notification to mitigate negative impacts.

1. Implement and enforce strict inactivity timeouts to automatically log users out after a period of inactivity.
2. Set an overall time limit for sessions, after which users must re-authenticate.
3. Restrict sessions to a single device or location at a time, or require additional verification for access from new locations or devices.

For detailed advice on how to mitigate threats related to the card, see the [ASVS and OWASP Developer Guide requirements ](#mapping 'ASVS and OWASP Developer Guide requirements [internal]') in the table below.
