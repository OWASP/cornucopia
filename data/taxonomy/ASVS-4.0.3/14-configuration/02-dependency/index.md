#  Dependency
## V14.2.1
Verify that all components are up to date, preferably using a dependency checker during build or compile time. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [1026](https://cwe.mitre.org/data/definitions/1026)
## V14.2.2
Verify that all unneeded features, documentation, sample applications and configurations are removed.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [1002](https://cwe.mitre.org/data/definitions/1002)
## V14.2.3
Verify that if application assets, such as JavaScript libraries, CSS or web fonts, are hosted externally on a Content Delivery Network (CDN) or external provider, Subresource Integrity (SRI) is used to validate the integrity of the asset.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [829](https://cwe.mitre.org/data/definitions/829)
## V14.2.4
Verify that third party components come from pre-defined, trusted and continually maintained repositories. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [829](https://cwe.mitre.org/data/definitions/829)
## V14.2.5
Verify that a Software Bill of Materials (SBOM) is maintained of all third party libraries in use. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [](https://cwe.mitre.org/data/definitions/)
## V14.2.6
Verify that the attack surface is reduced by sandboxing or encapsulating third party libraries to expose only the required behaviour into the application. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [265](https://cwe.mitre.org/data/definitions/265)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
