# Public Key Cryptography

## V11.6.1

Verify that only approved cryptographic algorithms and modes of operation are used for key generation and seeding, and digital signature generation and verification. Key generation algorithms must not generate insecure keys vulnerable to known attacks, for example, RSA keys which are vulnerable to Fermat factorization.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [20](/taxonomy/capec-3.9/20/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [233](/taxonomy/capec-3.9/233/index.md), [272](/taxonomy/capec-3.9/272/index.md), [39](/taxonomy/capec-3.9/39/index.md), [473](/taxonomy/capec-3.9/473/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [68](/taxonomy/capec-3.9/68/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## V11.6.2

Verify that approved cryptographic algorithms are used for key exchange (such as Diffie-Hellman) with a focus on ensuring that key exchange mechanisms use secure parameters. This will prevent attacks on the key establishment process which could lead to adversary-in-the-middle attacks or cryptographic breaks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [20](/taxonomy/capec-3.9/20/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [233](/taxonomy/capec-3.9/233/index.md), [272](/taxonomy/capec-3.9/272/index.md), [39](/taxonomy/capec-3.9/39/index.md), [473](/taxonomy/capec-3.9/473/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [68](/taxonomy/capec-3.9/68/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
