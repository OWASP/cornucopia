#  Credential Recovery
## V2.5.1
Verify that a system generated initial activation or recovery secret is not sent in clear text to the user. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [640](https://cwe.mitre.org/data/definitions/640)
## V2.5.2
Verify password hints or knowledge-based authentication (so-called "secret questions") are not present.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [640](https://cwe.mitre.org/data/definitions/640)
## V2.5.3
Verify password credential recovery does not reveal the current password in any way. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [640](https://cwe.mitre.org/data/definitions/640)
## V2.5.4
Verify shared or default accounts are not present (e.g. "root", "admin", or "sa").
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [16](https://cwe.mitre.org/data/definitions/16)
## V2.5.5
Verify that if an authentication factor is changed or replaced, that the user is notified of this event.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [304](https://cwe.mitre.org/data/definitions/304)
## V2.5.6
Verify forgotten password, and other recovery paths use a secure recovery mechanism, such as time-based OTP (TOTP) or other soft token, mobile push, or another offline recovery mechanism. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [640](https://cwe.mitre.org/data/definitions/640)
## V2.5.7
Verify that if OTP or multi-factor authentication factors are lost, that evidence of identity proofing is performed at the same level as during enrollment.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
