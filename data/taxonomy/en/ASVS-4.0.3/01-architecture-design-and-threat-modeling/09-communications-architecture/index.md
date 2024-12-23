#  Communications Architecture
## V1.9.1
Verify the application encrypts communications between components, particularly when these components are in different containers, systems, sites, or cloud providers. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [319](https://cwe.mitre.org/data/definitions/319)
## V1.9.2
Verify that application components verify the authenticity of each side in a communication link to prevent person-in-the-middle attacks. For example, application components should validate TLS certificates and chains.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [295](https://cwe.mitre.org/data/definitions/295)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
