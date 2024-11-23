#  Algorithms
## V6.2.1
Verify that all cryptographic modules fail securely, and errors are handled in a way that does not enable Padding Oracle attacks.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [310](https://cwe.mitre.org/data/definitions/310)
## V6.2.2
Verify that industry proven or government approved cryptographic algorithms, modes, and libraries are used, instead of custom coded cryptography. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [327](https://cwe.mitre.org/data/definitions/327)
## V6.2.3
Verify that encryption initialization vector, cipher configuration, and block modes are configured securely using the latest advice.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [326](https://cwe.mitre.org/data/definitions/326)
## V6.2.4
Verify that random number, encryption or hashing algorithms, key lengths, rounds, ciphers or modes, can be reconfigured, upgraded, or swapped at any time, to protect against cryptographic breaks. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [326](https://cwe.mitre.org/data/definitions/326)
## V6.2.5
Verify that known insecure block modes (i.e. ECB, etc.), padding modes (i.e. PKCS#1 v1.5, etc.), ciphers with small block sizes (i.e. Triple-DES, Blowfish, etc.), and weak hashing algorithms (i.e. MD5, SHA1, etc.) are not used unless required for backwards compatibility.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [326](https://cwe.mitre.org/data/definitions/326)
## V6.2.6
Verify that nonces, initialization vectors, and other single use numbers must not be used more than once with a given encryption key. The method of generation must be appropriate for the algorithm being used.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [326](https://cwe.mitre.org/data/definitions/326)
## V6.2.7
Verify that encrypted data is authenticated via signatures, authenticated cipher modes, or HMAC to ensure that ciphertext is not altered by an unauthorized party.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [326](https://cwe.mitre.org/data/definitions/326)
## V6.2.8
Verify that all cryptographic operations are constant-time, with no 'short-circuit' operations in comparisons, calculations, or returns, to avoid leaking information.
Level 1 required: False
Level 2 required: False
Level 3 required: True
CWE: [385](https://cwe.mitre.org/data/definitions/385)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
