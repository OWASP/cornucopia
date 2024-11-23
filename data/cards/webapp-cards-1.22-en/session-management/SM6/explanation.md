### Scenario: Gary’s Session Takeover Tactics 
Picture a scenario where Gary exploits session management weaknesses to take over a user's session. He takes advantage of: 

1. **Long or No Inactivity Timeout:** Sessions remain active despite prolonged user inactivity. 

2. **Extended or No Overall Session Time Limit:** Sessions do not have a defined expiration time. 

3. **Multi-Location Session Usage:** The system allows the same session to be used simultaneously from different devices or locations. 

### Example: 

Gary identifies that an online banking platform does not enforce inactivity timeouts. A user logs into their account but forgets to log out. The session remains active indefinitely, giving Gary an opportunity to access this session if the user’s device is left unattended or compromised. Additionally, the system’s allowance of the same session being used from multiple locations enables Gary to maintain access even when the legitimate user is active elsewhere. 

### Risks: 

This vulnerability can lead to unauthorized session takeovers, leading to potential data theft, financial loss, and privacy breaches. 

### Mitigation: 

- Implement and enforce strict inactivity timeouts to automatically log users out after a period of inactivity. 
- Set an overall time limit for sessions, after which users must re-authenticate. 
- Restrict sessions to a single device or location at a time, or require additional verification for access from new locations or devices. 