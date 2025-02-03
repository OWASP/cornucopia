#  File Execution
## V12.3.1
Verify that user-submitted filename metadata is not used directly by system or framework filesystems and that a URL API is used to protect against path traversal.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [22](https://cwe.mitre.org/data/definitions/22)
## V12.3.2
Verify that user-submitted filename metadata is validated or ignored to prevent the disclosure, creation, updating or removal of local files (LFI).
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [73](https://cwe.mitre.org/data/definitions/73)
## V12.3.3
Verify that user-submitted filename metadata is validated or ignored to prevent the disclosure or execution of remote files via Remote File Inclusion (RFI) or Server-side Request Forgery (SSRF) attacks.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [98](https://cwe.mitre.org/data/definitions/98)
## V12.3.4
Verify that the application protects against Reflective File Download (RFD) by validating or ignoring user-submitted filenames in a JSON, JSONP, or URL parameter, the response Content-Type header should be set to text/plain, and the Content-Disposition header should have a fixed filename.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [641](https://cwe.mitre.org/data/definitions/641)
## V12.3.5
Verify that untrusted file metadata is not used directly with system API or libraries, to protect against OS command injection.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [78](https://cwe.mitre.org/data/definitions/78)
## V12.3.6
Verify that the application does not include and execute functionality from untrusted sources, such as unverified content distribution networks, JavaScript libraries, node npm libraries, or server-side DLLs.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [829](https://cwe.mitre.org/data/definitions/829)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
