#  General Data Protection
## V8.1.1
Verify the application protects sensitive data from being cached in server components such as load balancers and application caches.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [524](https://cwe.mitre.org/data/definitions/524)
## V8.1.2
Verify that all cached or temporary copies of sensitive data stored on the server are protected from unauthorized access or purged/invalidated after the authorized user accesses the sensitive data.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [524](https://cwe.mitre.org/data/definitions/524)
## V8.1.3
Verify the application minimizes the number of parameters in a request, such as hidden fields, Ajax variables, cookies and header values.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [233](https://cwe.mitre.org/data/definitions/233)
## V8.1.4
Verify the application can detect and alert on abnormal numbers of requests, such as by IP, user, total per hour or day, or whatever makes sense for the application.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [770](https://cwe.mitre.org/data/definitions/770)
## V8.1.5
Verify that regular backups of important data are performed and that test restoration of data is performed.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [19](https://cwe.mitre.org/data/definitions/19)
## V8.1.6
Verify that backups are stored securely to prevent data from being stolen or corrupted.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [19](https://cwe.mitre.org/data/definitions/19)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
