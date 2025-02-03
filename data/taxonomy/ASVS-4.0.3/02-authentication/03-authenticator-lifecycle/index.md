#  Authenticator Lifecycle
## V2.3.1
Verify system generated initial passwords or activation codes SHOULD be securely randomly generated, SHOULD be at least 6 characters long, and MAY contain letters and numbers, and expire after a short period of time. These initial secrets must not be permitted to become the long term password.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [330](https://cwe.mitre.org/data/definitions/330)
## V2.3.2
Verify that enrollment and use of user-provided authentication devices are supported, such as a U2F or FIDO tokens.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)
## V2.3.3
Verify that renewal instructions are sent with sufficient time to renew time bound authenticators.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [287](https://cwe.mitre.org/data/definitions/287)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
