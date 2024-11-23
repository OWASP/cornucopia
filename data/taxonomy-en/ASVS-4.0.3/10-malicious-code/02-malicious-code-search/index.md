#  Malicious Code Search
## V10.2.1
Verify that the application source code and third party libraries do not contain unauthorized phone home or data collection capabilities. Where such functionality exists, obtain the user's permission for it to operate before collecting any data.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [359](https://cwe.mitre.org/data/definitions/359)
## V10.2.2
Verify that the application does not ask for unnecessary or excessive permissions to privacy related features or sensors, such as contacts, cameras, microphones, or location.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [272](https://cwe.mitre.org/data/definitions/272)
## V10.2.3
Verify that the application source code and third party libraries do not contain back doors, such as hard-coded or additional undocumented accounts or keys, code obfuscation, undocumented binary blobs, rootkits, or anti-debugging, insecure debugging features, or otherwise out of date, insecure, or hidden functionality that could be used maliciously if discovered.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [507](https://cwe.mitre.org/data/definitions/507)
## V10.2.4
Verify that the application source code and third party libraries do not contain time bombs by searching for date and time related functions.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [511](https://cwe.mitre.org/data/definitions/511)
## V10.2.5
Verify that the application source code and third party libraries do not contain malicious code, such as salami attacks, logic bypasses, or logic bombs.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [511](https://cwe.mitre.org/data/definitions/511)
## V10.2.6
Verify that the application source code and third party libraries do not contain Easter eggs or any other potentially unwanted functionality.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [507](https://cwe.mitre.org/data/definitions/507)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
