#  Access Control Architecture
## V1.4.1
Verify that trusted enforcement points, such as access control gateways, servers, and serverless functions, enforce access controls. Never enforce access controls on the client.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [602](https://cwe.mitre.org/data/definitions/602)
## V1.4.2
[DELETED, NOT ACTIONABLE]
Level 1 required: False
Level 2 required: False
Level 3 required: False
CWE: [](https://cwe.mitre.org/data/definitions/)
## V1.4.3
[DELETED, DUPLICATE OF 4.1.3]
Level 1 required: False
Level 2 required: False
Level 3 required: False
CWE: [](https://cwe.mitre.org/data/definitions/)
## V1.4.4
Verify the application uses a single and well-vetted access control mechanism for accessing protected data and resources. All requests must pass through this single mechanism to avoid copy and paste or insecure alternative paths. ([C7](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [284](https://cwe.mitre.org/data/definitions/284)
## V1.4.5
Verify that attribute or feature-based access control is used whereby the code checks the user's authorization for a feature/data item rather than just their role. Permissions should still be allocated using roles. ([C7](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [275](https://cwe.mitre.org/data/definitions/275)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
