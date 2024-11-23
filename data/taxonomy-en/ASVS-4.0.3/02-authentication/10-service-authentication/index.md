#  Service Authentication
## V2.10.1
Verify that intra-service secrets do not rely on unchanging credentials such as passwords, API keys or shared accounts with privileged access.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [287](https://cwe.mitre.org/data/definitions/287)
## V2.10.2
Verify that if passwords are required for service authentication, the service account used is not a default credential. (e.g. root/root or admin/admin are default in some services during installation).
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [255](https://cwe.mitre.org/data/definitions/255)
## V2.10.3
Verify that passwords are stored with sufficient protection to prevent offline recovery attacks, including local system access.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [522](https://cwe.mitre.org/data/definitions/522)
## V2.10.4
Verify passwords, integrations with databases and third-party systems, seeds and internal secrets, and API keys are managed securely and not included in the source code or stored within source code repositories. Such storage SHOULD resist offline attacks. The use of a secure software key store (L1), hardware TPM, or an HSM (L3) is recommended for password storage.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [798](https://cwe.mitre.org/data/definitions/798)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
