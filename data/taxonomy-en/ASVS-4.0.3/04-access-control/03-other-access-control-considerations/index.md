#  Other Access Control Considerations
## V4.3.1
Verify administrative interfaces use appropriate multi-factor authentication to prevent unauthorized use.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [419](https://cwe.mitre.org/data/definitions/419)
## V4.3.2
Verify that directory browsing is disabled unless deliberately desired. Additionally, applications should not allow discovery or disclosure of file or directory metadata, such as Thumbs.db, .DS_Store, .git or .svn folders.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [548](https://cwe.mitre.org/data/definitions/548)
## V4.3.3
Verify the application has additional authorization (such as step up or adaptive authentication) for lower value systems, and / or segregation of duties for high value applications to enforce anti-fraud controls as per the risk of application and past fraud.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [732](https://cwe.mitre.org/data/definitions/732)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
