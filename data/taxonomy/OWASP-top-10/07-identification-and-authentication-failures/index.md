# Identification and Authentication Failures 
## Description
Confirmation of the user's identity, authentication, and session management is critical to protect against authentication-related attacks. There may be authentication weaknesses if the application:

- Permits automated attacks such as credential stuffing, where the attacker has a list of valid usernames and passwords.
- Permits brute force or other automated attacks.
- Permits default, weak, or well-known passwords, such as "Password1" or "admin/admin".
- Uses weak or ineffective credential recovery and forgot-password processes, such as "knowledge-based answers," which cannot be made safe.
- Uses plain text, encrypted, or weakly hashed passwords data stores (see A02:2021-Cryptographic Failures).
- Has missing or ineffective multi-factor authentication.
- Exposes session identifier in the URL.
- Reuse session identifier after successful login.
- Does not correctly invalidate Session IDs. User sessions or authentication tokens (mainly single sign-on (SSO) tokens) aren't properly invalidated during logout or a period of inactivity.

## How to Prevent
- Where possible, implement multi-factor authentication to prevent automated credential stuffing, brute force, and stolen credential reuse attacks.
- Do not ship or deploy with any default credentials, particularly for admin users.
- Implement weak password checks, such as testing new or changed passwords against the top 10,000 worst passwords list.
- Align password length, complexity, and rotation policies with National Institute of Standards and Technology (NIST) 800-63b's guidelines in section 5.1.1 for Memorized Secrets or other modern, evidence-based password policies.
- Ensure registration, credential recovery, and API pathways are hardened against account enumeration attacks by using the same messages for all outcomes.
- Limit or increasingly delay failed login attempts, but be careful not to create a denial of service scenario. Log all failures and alert administrators when credential stuffing, brute force, or other attacks are detected.
- Use a server-side, secure, built-in session manager that generates a new random session ID with high entropy after login. Session identifier should not be in the URL, be securely stored, and invalidated after logout, idle, and absolute timeouts.

[Source: OWASP TOP 10 Identification and Authentication Failures ](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

## Cheatsheets
[Identification and Authentication Failures Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a072021-identification-and-authentication-failures)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
- [Data-validation-&-encoding 3](/data-validation-&-encoding/3)
- [Data-validation-&-encoding 5](/data-validation-&-encoding/5)
- [Data-validation-&-encoding 7](/data-validation-&-encoding/7)
- [Data-validation-&-encoding 9](/data-validation-&-encoding/9)
- [Data-validation-&-encoding 10](/data-validation-&-encoding/10)
- [Data-validation-&-encoding K](/data-validation-&-encoding/K)

### Authentication
- [Authentication 2](/authentication/2)
- [Authentication 3](/authentication/3)
- [Authentication 4](/authentication/4)
- [Authentication 5](/authentication/5)
- [Authentication 6](/authentication/6)
- [Authentication 7](/authentication/7)
- [Authentication 8](/authentication/8)
- [Authentication 9](/authentication/9)
- [Authentication 10](/authentication/10)
- [Authentication J](/authentication/J)
- [Authentication Q](/authentication/Q)
- [Authentication K](/authentication/K)

### Session-management
- [Session-management 3](/session-management/3)
- [Session-management 6](/session-management/6)
- [Session-management 7](/session-management/7)
- [Session-management 8](/session-management/8)
- [Session-management J](/session-management/J)
- [Session-management Q](/session-management/Q)
- [Session-management K](/session-management/K)

### Authorization
- [Authorization 3](/authorization/3)
- [Authorization 4](/authorization/4)
- [Authorization 5](/authorization/5)
- [Authorization 9](/authorization/9)

### Cornucopia
- [Cornucopia 2](/cornucopia/2)
- [Cornucopia 5](/cornucopia/5)
- [Cornucopia 8](/cornucopia/8)
- [Cornucopia 9](/cornucopia/9)
- [Cornucopia K](/cornucopia/K)
