#  Generic Web Service Security
## V13.1.1
Verify that all application components use the same encodings and parsers to avoid parsing attacks that exploit different URI or file parsing behavior that could be used in SSRF and RFI attacks.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [116](https://cwe.mitre.org/data/definitions/116)
## V13.1.2
[DELETED, DUPLICATE OF 4.3.1]
Level 1 required: False
Level 2 required: False
Level 3 required: False
CWE: [](https://cwe.mitre.org/data/definitions/)
## V13.1.3
Verify API URLs do not expose sensitive information, such as the API key, session tokens etc.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [598](https://cwe.mitre.org/data/definitions/598)
## V13.1.4
Verify that authorization decisions are made at both the URI, enforced by programmatic or declarative security at the controller or router, and at the resource level, enforced by model-based permissions.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [285](https://cwe.mitre.org/data/definitions/285)
## V13.1.5
Verify that requests containing unexpected or missing content types are rejected with appropriate headers (HTTP response status 406 Unacceptable or 415 Unsupported Media Type).
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [434](https://cwe.mitre.org/data/definitions/434)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
