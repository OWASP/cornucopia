#  Secure File Upload Architecture
## V1.12.1
[DELETED, DUPLICATE OF 12.4.1]
Level 1 required: False
Level 2 required: False
Level 3 required: False
CWE: [](https://cwe.mitre.org/data/definitions/)
## V1.12.2
Verify that user-uploaded files - if required to be displayed or downloaded from the application - are served by either octet stream downloads, or from an unrelated domain, such as a cloud file storage bucket. Implement a suitable Content Security Policy (CSP) to reduce the risk from XSS vectors or other attacks from the uploaded file.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [646](https://cwe.mitre.org/data/definitions/646)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
