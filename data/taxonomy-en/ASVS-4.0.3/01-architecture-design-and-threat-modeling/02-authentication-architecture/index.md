#  Authentication Architecture
## V1.2.1
Verify the use of unique or special low-privilege operating system accounts for all application components, services, and servers. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [250](https://cwe.mitre.org/data/definitions/250)
## V1.2.2
Verify that communications between application components, including APIs, middleware and data layers, are authenticated. Components should have the least necessary privileges needed. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [306](https://cwe.mitre.org/data/definitions/306)
## V1.2.3
Verify that the application uses a single vetted authentication mechanism that is known to be secure, can be extended to include strong authentication, and has sufficient logging and monitoring to detect account abuse or breaches.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [306](https://cwe.mitre.org/data/definitions/306)
## V1.2.4
Verify that all authentication pathways and identity management APIs implement consistent authentication security control strength, such that there are no weaker alternatives per the risk of the application.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [306](https://cwe.mitre.org/data/definitions/306)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
