# Session Termination
## V7.4.1
Verify that when session termination is triggered (such as logout or expiration), the application disallows any further use of the session. For reference tokens or stateful sessions, this means invalidating the session data at the application backend. Applications using self-contained tokens will need a solution such as maintaining a list of terminated tokens, disallowing tokens produced before a per-user date and time or rotating a per-user signing key.
Required for Level 1, 2 and 3
## V7.4.2
Verify that the application terminates all active sessions when a user account is disabled or deleted (such as an employee leaving the company).
Required for Level 1, 2 and 3
## V7.4.3
Verify that the application gives the option to terminate all other active sessions after a successful change or removal of any authentication factor (including password change via reset or recovery and, if present, an MFA settings update).
Required for Level 2 and 3
## V7.4.4
Verify that all pages that require authentication have easy and visible access to logout functionality.
Required for Level 2 and 3
## V7.4.5
Verify that application administrators are able to terminate active sessions for an individual user or for all users.
Required for Level 2 and 3
## Disclaimer
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
