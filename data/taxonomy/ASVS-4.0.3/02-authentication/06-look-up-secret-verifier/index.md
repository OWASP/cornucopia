#  Look-up Secret Verifier
## V2.6.1
Verify that lookup secrets can be used only once.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)
## V2.6.2
Verify that lookup secrets have sufficient randomness (112 bits of entropy), or if less than 112 bits of entropy, salted with a unique and random 32-bit salt and hashed with an approved one-way hash.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [330](https://cwe.mitre.org/data/definitions/330)
## V2.6.3
Verify that lookup secrets are resistant to offline attacks, such as predictable values.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [310](https://cwe.mitre.org/data/definitions/310)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
