#  Cookie-based Session Management
## V3.4.1
Verify that cookie-based session tokens have the 'Secure' attribute set. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [614](https://cwe.mitre.org/data/definitions/614)
## V3.4.2
Verify that cookie-based session tokens have the 'HttpOnly' attribute set. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [1004](https://cwe.mitre.org/data/definitions/1004)
## V3.4.3
Verify that cookie-based session tokens utilize the 'SameSite' attribute to limit exposure to cross-site request forgery attacks. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [1275](https://cwe.mitre.org/data/definitions/1275)
## V3.4.4
Verify that cookie-based session tokens use the "__Host-" prefix so cookies are only sent to the host that initially set the cookie.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [16](https://cwe.mitre.org/data/definitions/16)
## V3.4.5
Verify that if the application is published under a domain name with other applications that set or use session cookies that might disclose the session cookies, set the path attribute in cookie-based session tokens using the most precise path possible. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [16](https://cwe.mitre.org/data/definitions/16)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
