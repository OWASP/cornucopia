#  Input Validation
## V5.1.1
Verify that the application has defenses against HTTP parameter pollution attacks, particularly if the application framework makes no distinction about the source of request parameters (GET, POST, cookies, headers, or environment variables).
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [235](https://cwe.mitre.org/data/definitions/235)
## V5.1.2
Verify that frameworks protect against mass parameter assignment attacks, or that the application has countermeasures to protect against unsafe parameter assignment, such as marking fields private or similar. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [915](https://cwe.mitre.org/data/definitions/915)
## V5.1.3
Verify that all input (HTML form fields, REST requests, URL parameters, HTTP headers, cookies, batch files, RSS feeds, etc) is validated using positive validation (allow lists). ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [20](https://cwe.mitre.org/data/definitions/20)
## V5.1.4
Verify that structured data is strongly typed and validated against a defined schema including allowed characters, length and pattern (e.g. credit card numbers, e-mail addresses, telephone numbers, or validating that two related fields are reasonable, such as checking that suburb and zip/postcode match). ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [20](https://cwe.mitre.org/data/definitions/20)
## V5.1.5
Verify that URL redirects and forwards only allow destinations which appear on an allow list, or show a warning when redirecting to potentially untrusted content.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [601](https://cwe.mitre.org/data/definitions/601)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
