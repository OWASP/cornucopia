#  Session Termination
## V3.3.1
Verify that logout and expiration invalidate the session token, such that the back button or a downstream relying party does not resume an authenticated session, including across relying parties. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [613](https://cwe.mitre.org/data/definitions/613)
## V3.3.2
If authenticators permit users to remain logged in, verify that re-authentication occurs periodically both when actively used or after an idle period. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [613](https://cwe.mitre.org/data/definitions/613)
## V3.3.3
Verify that the application gives the option to terminate all other active sessions after a successful password change (including change via password reset/recovery), and that this is effective across the application, federated login (if present), and any relying parties.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [613](https://cwe.mitre.org/data/definitions/613)
## V3.3.4
Verify that users are able to view and (having re-entered login credentials) log out of any or all currently active sessions and devices.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [613](https://cwe.mitre.org/data/definitions/613)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
