#  Deserialization Prevention
## V5.5.1
Verify that serialized objects use integrity checks or are encrypted to prevent hostile object creation or data tampering. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [502](https://cwe.mitre.org/data/definitions/502)
## V5.5.2
Verify that the application correctly restricts XML parsers to only use the most restrictive configuration possible and to ensure that unsafe features such as resolving external entities are disabled to prevent XML eXternal Entity (XXE) attacks.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [611](https://cwe.mitre.org/data/definitions/611)
## V5.5.3
Verify that deserialization of untrusted data is avoided or is protected in both custom code and third-party libraries (such as JSON, XML and YAML parsers).
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [502](https://cwe.mitre.org/data/definitions/502)
## V5.5.4
Verify that when parsing JSON in browsers or JavaScript-based backends, JSON.parse is used to parse the JSON document. Do not use eval() to parse JSON.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [95](https://cwe.mitre.org/data/definitions/95)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
