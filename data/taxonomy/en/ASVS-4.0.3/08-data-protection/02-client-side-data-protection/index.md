#  Client-side Data Protection
## V8.2.1
Verify the application sets sufficient anti-caching headers so that sensitive data is not cached in modern browsers.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [525](https://cwe.mitre.org/data/definitions/525)
## V8.2.2
Verify that data stored in browser storage (such as localStorage, sessionStorage, IndexedDB, or cookies) does not contain sensitive data.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [922](https://cwe.mitre.org/data/definitions/922)
## V8.2.3
Verify that authenticated data is cleared from client storage, such as the browser DOM, after the client or session is terminated.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [922](https://cwe.mitre.org/data/definitions/922)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
