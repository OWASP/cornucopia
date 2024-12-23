#  Input and Output Architecture
## V1.5.1
Verify that input and output requirements clearly define how to handle and process data based on type, content, and applicable laws, regulations, and other policy compliance.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [1029](https://cwe.mitre.org/data/definitions/1029)
## V1.5.2
Verify that serialization is not used when communicating with untrusted clients. If this is not possible, ensure that adequate integrity controls (and possibly encryption if sensitive data is sent) are enforced to prevent deserialization attacks including object injection.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [502](https://cwe.mitre.org/data/definitions/502)
## V1.5.3
Verify that input validation is enforced on a trusted service layer. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [602](https://cwe.mitre.org/data/definitions/602)
## V1.5.4
Verify that output encoding occurs close to or by the interpreter for which it is intended. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [116](https://cwe.mitre.org/data/definitions/116)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
