#  Sensitive Private Data
## V8.3.1
Verify that sensitive data is sent to the server in the HTTP message body or headers, and that query string parameters from any HTTP verb do not contain sensitive data.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [319](https://cwe.mitre.org/data/definitions/319)
## V8.3.2
Verify that users have a method to remove or export their data on demand.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [212](https://cwe.mitre.org/data/definitions/212)
## V8.3.3
Verify that users are provided clear language regarding collection and use of supplied personal information and that users have provided opt-in consent for the use of that data before it is used in any way.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [285](https://cwe.mitre.org/data/definitions/285)
## V8.3.4
Verify that all sensitive data created and processed by the application has been identified, and ensure that a policy is in place on how to deal with sensitive data. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [200](https://cwe.mitre.org/data/definitions/200)
## V8.3.5
Verify accessing sensitive data is audited (without logging the sensitive data itself), if the data is collected under relevant data protection directives or where logging of access is required.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [532](https://cwe.mitre.org/data/definitions/532)
## V8.3.6
Verify that sensitive information contained in memory is overwritten as soon as it is no longer required to mitigate memory dumping attacks, using zeroes or random data.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [226](https://cwe.mitre.org/data/definitions/226)
## V8.3.7
Verify that sensitive or private information that is required to be encrypted, is encrypted using approved algorithms that provide both confidentiality and integrity. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [327](https://cwe.mitre.org/data/definitions/327)
## V8.3.8
Verify that sensitive personal information is subject to data retention classification, such that old or out of date data is deleted automatically, on a schedule, or as the situation requires.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [285](https://cwe.mitre.org/data/definitions/285)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
