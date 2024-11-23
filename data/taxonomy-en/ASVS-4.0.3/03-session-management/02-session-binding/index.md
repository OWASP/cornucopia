#  Session Binding
## V3.2.1
Verify the application generates a new session token on user authentication. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [384](https://cwe.mitre.org/data/definitions/384)
## V3.2.2
Verify that session tokens possess at least 64 bits of entropy. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [331](https://cwe.mitre.org/data/definitions/331)
## V3.2.3
Verify the application only stores session tokens in the browser using secure methods such as appropriately secured cookies (see section 3.4) or HTML 5 session storage.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [539](https://cwe.mitre.org/data/definitions/539)
## V3.2.4
Verify that session tokens are generated using approved cryptographic algorithms. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [331](https://cwe.mitre.org/data/definitions/331)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
