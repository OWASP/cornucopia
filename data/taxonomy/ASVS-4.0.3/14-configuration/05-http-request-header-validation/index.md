#  HTTP Request Header Validation
## V14.5.1
Verify that the application server only accepts the HTTP methods in use by the application/API, including pre-flight OPTIONS, and logs/alerts on any requests that are not valid for the application context.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [749](https://cwe.mitre.org/data/definitions/749)
## V14.5.2
Verify that the supplied Origin header is not used for authentication or access control decisions, as the Origin header can easily be changed by an attacker.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [346](https://cwe.mitre.org/data/definitions/346)
## V14.5.3
Verify that the Cross-Origin Resource Sharing (CORS) Access-Control-Allow-Origin header uses a strict allow list of trusted domains and subdomains to match against and does not support the "null" origin.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [346](https://cwe.mitre.org/data/definitions/346)
## V14.5.4
Verify that HTTP headers added by a trusted proxy or SSO devices, such as a bearer token, are authenticated by the application.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [306](https://cwe.mitre.org/data/definitions/306)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
