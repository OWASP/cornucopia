#  Log Content
## V7.1.1
Verify that the application does not log credentials or payment details. Session tokens should only be stored in logs in an irreversible, hashed form. ([C9, C10](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [532](https://cwe.mitre.org/data/definitions/532)
## V7.1.2
Verify that the application does not log other sensitive data as defined under local privacy laws or relevant security policy. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [532](https://cwe.mitre.org/data/definitions/532)
## V7.1.3
Verify that the application logs security relevant events including successful and failed authentication events, access control failures, deserialization failures and input validation failures. ([C5, C7](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [778](https://cwe.mitre.org/data/definitions/778)
## V7.1.4
Verify that each log event includes necessary information that would allow for a detailed investigation of the timeline when an event happens. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [778](https://cwe.mitre.org/data/definitions/778)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
