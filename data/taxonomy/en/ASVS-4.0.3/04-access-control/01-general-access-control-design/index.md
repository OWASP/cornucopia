#  General Access Control Design
## V4.1.1
Verify that the application enforces access control rules on a trusted service layer, especially if client-side access control is present and could be bypassed.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [602](https://cwe.mitre.org/data/definitions/602)
## V4.1.2
Verify that all user and data attributes and policy information used by access controls cannot be manipulated by end users unless specifically authorized.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [639](https://cwe.mitre.org/data/definitions/639)
## V4.1.3
Verify that the principle of least privilege exists - users should only be able to access functions, data files, URLs, controllers, services, and other resources, for which they possess specific authorization. This implies protection against spoofing and elevation of privilege. ([C7](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [285](https://cwe.mitre.org/data/definitions/285)
## V4.1.4
[DELETED, DUPLICATE OF 4.1.3]
Level 1 required: False
Level 2 required: False
Level 3 required: False
CWE: [](https://cwe.mitre.org/data/definitions/)
## V4.1.5
Verify that access controls fail securely including when an exception occurs. ([C10](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [285](https://cwe.mitre.org/data/definitions/285)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
