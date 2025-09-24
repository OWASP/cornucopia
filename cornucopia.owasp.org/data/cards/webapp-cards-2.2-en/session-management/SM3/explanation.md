## Scenario: Ryan’s Exploitation of Concurrent Sessions

Imagine a scenario where Ryan takes advantage of a system's leniency in allowing multiple concurrent sessions for a single account. This occurs because:

1. **Allowance of Multiple Active Sessions:** The system permits one user account to be logged in from multiple devices or locations at the same time.

### Example

Ryan discovers that a corporate network does not restrict the number of active sessions per user account. He obtains the login credentials of an employee and logs into the account while the legitimate user is also active. The system fails to detect or alert the concurrent usage, allowing Ryan to access sensitive information and perform unauthorized actions unnoticed.

## Threat Modeling

### STRIDE

This scenario falls under STRIDE: **Spoofing**.

**Spoofing** is about impersonating a legitimate user or system.
Ryan uses valid credentials to simultaneously access the account while the legitimate user is active, effectively impersonating the user in parallel.
The system’s failure to restrict or monitor concurrent sessions enables him to bypass control over who is acting as that user.

### What can go Wrong?

Allowing concurrent sessions without proper controls can lead to unauthorized access and exploitation of user accounts, potentially compromising data security and privacy.

### What are you going to do about it?

- Implement a policy to restrict or carefully monitor concurrent sessions. Options include limiting the number of simultaneous sessions per user or requiring additional verification for new sessions.
- Set up alerts for unusual patterns of concurrent access, such as logins from geographically distant locations within a short timeframe.
- Regularly audit session management policies to ensure they effectively protect against unauthorized concurrent access. 
