# Public Key Cryptography

## V11.6.1

Verify that only approved cryptographic algorithms and modes of operation are used for key generation and seeding, and digital signature generation and verification. Key generation algorithms must not generate insecure keys vulnerable to known attacks, for example, RSA keys which are vulnerable to Fermat factorization.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [233](/taxonomy/capec-3.9/233), [272](/taxonomy/capec-3.9/272), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [68](/taxonomy/capec-3.9/68), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## V11.6.2

Verify that approved cryptographic algorithms are used for key exchange (such as Diffie-Hellman) with a focus on ensuring that key exchange mechanisms use secure parameters. This will prevent attacks on the key establishment process which could lead to adversary-in-the-middle attacks or cryptographic breaks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [233](/taxonomy/capec-3.9/233), [272](/taxonomy/capec-3.9/272), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [68](/taxonomy/capec-3.9/68), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
