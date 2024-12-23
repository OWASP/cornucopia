#  General Authenticator Security
## V2.2.1
Verify that anti-automation controls are effective at mitigating breached credential testing, brute force, and account lockout attacks. Such controls include blocking the most common breached passwords, soft lockouts, rate limiting, CAPTCHA, ever increasing delays between attempts, IP address restrictions, or risk-based restrictions such as location, first login on a device, recent attempts to unlock the account, or similar. Verify that no more than 100 failed attempts per hour is possible on a single account.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [307](https://cwe.mitre.org/data/definitions/307)
## V2.2.2
Verify that the use of weak authenticators (such as SMS and email) is limited to secondary verification and transaction approval and not as a replacement for more secure authentication methods. Verify that stronger methods are offered before weak methods, users are aware of the risks, or that proper measures are in place to limit the risks of account compromise.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [304](https://cwe.mitre.org/data/definitions/304)
## V2.2.3
Verify that secure notifications are sent to users after updates to authentication details, such as credential resets, email or address changes, logging in from unknown or risky locations. The use of push notifications - rather than SMS or email - is preferred, but in the absence of push notifications, SMS or email is acceptable as long as no sensitive information is disclosed in the notification.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [620](https://cwe.mitre.org/data/definitions/620)
## V2.2.4
Verify impersonation resistance against phishing, such as the use of multi-factor authentication, cryptographic devices with intent (such as connected keys with a push to authenticate), or at higher AAL levels, client-side certificates.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)
## V2.2.5
Verify that where a Credential Service Provider (CSP) and the application verifying authentication are separated, mutually authenticated TLS is in place between the two endpoints.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [319](https://cwe.mitre.org/data/definitions/319)
## V2.2.6
Verify replay resistance through the mandated use of One-time Passwords (OTP) devices, cryptographic authenticators, or lookup codes.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)
## V2.2.7
Verify intent to authenticate by requiring the entry of an OTP token or user-initiated action such as a button press on a FIDO hardware key.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
