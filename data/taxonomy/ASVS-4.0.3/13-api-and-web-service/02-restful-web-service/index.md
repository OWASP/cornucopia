#  RESTful Web Service
## V13.2.1
Verify that enabled RESTful HTTP methods are a valid choice for the user or action, such as preventing normal users using DELETE or PUT on protected API or resources.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [650](https://cwe.mitre.org/data/definitions/650)
## V13.2.2
Verify that JSON schema validation is in place and verified before accepting input.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [20](https://cwe.mitre.org/data/definitions/20)
## V13.2.3
Verify that RESTful web services that utilize cookies are protected from Cross-Site Request Forgery via the use of at least one or more of the following: double submit cookie pattern, CSRF nonces, or Origin request header checks.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [352](https://cwe.mitre.org/data/definitions/352)
## V13.2.4
[DELETED, DUPLICATE OF 11.1.4]
Level 1 required: False
Level 2 required: False
Level 3 required: False
CWE: [](https://cwe.mitre.org/data/definitions/)
## V13.2.5
Verify that REST services explicitly check the incoming Content-Type to be the expected one, such as application/xml or application/json.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [436](https://cwe.mitre.org/data/definitions/436)
## V13.2.6
Verify that the message headers and payload are trustworthy and not modified in transit. Requiring strong encryption for transport (TLS only) may be sufficient in many cases as it provides both confidentiality and integrity protection. Per-message digital signatures can provide additional assurance on top of the transport protections for high-security applications but bring with them additional complexity and risks to weigh against the benefits.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [345](https://cwe.mitre.org/data/definitions/345)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
