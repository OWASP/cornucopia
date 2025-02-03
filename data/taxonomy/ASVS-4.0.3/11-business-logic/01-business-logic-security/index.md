#  Business Logic Security
## V11.1.1
Verify that the application will only process business logic flows for the same user in sequential step order and without skipping steps.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [841](https://cwe.mitre.org/data/definitions/841)
## V11.1.2
Verify that the application will only process business logic flows with all steps being processed in realistic human time, i.e. transactions are not submitted too quickly.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [799](https://cwe.mitre.org/data/definitions/799)
## V11.1.3
Verify the application has appropriate limits for specific business actions or transactions which are correctly enforced on a per user basis.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [770](https://cwe.mitre.org/data/definitions/770)
## V11.1.4
Verify that the application has anti-automation controls to protect against excessive calls such as mass data exfiltration, business logic requests, file uploads or denial of service attacks.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [770](https://cwe.mitre.org/data/definitions/770)
## V11.1.5
Verify the application has business logic limits or validation to protect against likely business risks or threats, identified using threat modeling or similar methodologies.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [841](https://cwe.mitre.org/data/definitions/841)
## V11.1.6
Verify that the application does not suffer from "Time Of Check to Time Of Use" (TOCTOU) issues or other race conditions for sensitive operations.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [367](https://cwe.mitre.org/data/definitions/367)
## V11.1.7
Verify that the application monitors for unusual events or activity from a business logic perspective. For example, attempts to perform actions out of order or actions which a normal user would never attempt. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [754](https://cwe.mitre.org/data/definitions/754)
## V11.1.8
Verify that the application has configurable alerting when automated attacks or unusual activity is detected.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [390](https://cwe.mitre.org/data/definitions/390)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
