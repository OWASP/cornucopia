#  Business Logic Architecture
## V1.11.1
Verify the definition and documentation of all application components in terms of the business or security functions they provide.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [1059](https://cwe.mitre.org/data/definitions/1059)
## V1.11.2
Verify that all high-value business logic flows, including authentication, session management and access control, do not share unsynchronized state.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [362](https://cwe.mitre.org/data/definitions/362)
## V1.11.3
Verify that all high-value business logic flows, including authentication, session management and access control are thread safe and resistant to time-of-check and time-of-use race conditions.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [367](https://cwe.mitre.org/data/definitions/367)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
