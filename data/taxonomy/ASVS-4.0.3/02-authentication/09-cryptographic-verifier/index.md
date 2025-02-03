#  Cryptographic Verifier
## V2.9.1
Verify that cryptographic keys used in verification are stored securely and protected against disclosure, such as using a Trusted Platform Module (TPM) or Hardware Security Module (HSM), or an OS service that can use this secure storage.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [320](https://cwe.mitre.org/data/definitions/320)
## V2.9.2
Verify that the challenge nonce is at least 64 bits in length, and statistically unique or unique over the lifetime of the cryptographic device.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [330](https://cwe.mitre.org/data/definitions/330)
## V2.9.3
Verify that approved cryptographic algorithms are used in the generation, seeding, and verification.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [327](https://cwe.mitre.org/data/definitions/327)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
