#  HTTP Security Headers
## V14.4.1
Verify that every HTTP response contains a Content-Type header. Also specify a safe character set (e.g., UTF-8, ISO-8859-1) if the content types are text/*, /+xml and application/xml. Content must match with the provided Content-Type header.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [173](https://cwe.mitre.org/data/definitions/173)
## V14.4.2
Verify that all API responses contain a Content-Disposition: attachment; filename="api.json" header (or other appropriate filename for the content type).
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [116](https://cwe.mitre.org/data/definitions/116)
## V14.4.3
Verify that a Content Security Policy (CSP) response header is in place that helps mitigate impact for XSS attacks like HTML, DOM, JSON, and JavaScript injection vulnerabilities.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [1021](https://cwe.mitre.org/data/definitions/1021)
## V14.4.4
Verify that all responses contain a X-Content-Type-Options: nosniff header.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [116](https://cwe.mitre.org/data/definitions/116)
## V14.4.5
Verify that a Strict-Transport-Security header is included on all responses and for all subdomains, such as Strict-Transport-Security: max-age=15724800; includeSubdomains.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [523](https://cwe.mitre.org/data/definitions/523)
## V14.4.6
Verify that a suitable Referrer-Policy header is included to avoid exposing sensitive information in the URL through the Referer header to untrusted parties.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [116](https://cwe.mitre.org/data/definitions/116)
## V14.4.7
Verify that the content of a web application cannot be embedded in a third-party site by default and that embedding of the exact resources is only allowed where necessary by using suitable Content-Security-Policy: frame-ancestors and X-Frame-Options response headers.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [1021](https://cwe.mitre.org/data/definitions/1021)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
