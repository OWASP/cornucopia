#  Random Values
## V6.3.1
Verify that all random numbers, random file names, random GUIDs, and random strings are generated using the cryptographic module's approved cryptographically secure random number generator when these random values are intended to be not guessable by an attacker.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [338](https://cwe.mitre.org/data/definitions/338)
## V6.3.2
Verify that random GUIDs are created using the GUID v4 algorithm, and a Cryptographically-secure Pseudo-random Number Generator (CSPRNG). GUIDs created using other pseudo-random number generators may be predictable.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [338](https://cwe.mitre.org/data/definitions/338)
## V6.3.3
Verify that random numbers are created with proper entropy even when the application is under heavy load, or that the application degrades gracefully in such circumstances.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [338](https://cwe.mitre.org/data/definitions/338)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
