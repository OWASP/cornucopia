# Secure Cryptography Implementation

## V11.2.1

Verify that industry-validated implementations (including libraries and hardware-accelerated implementations) are used for cryptographic operations.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [162](/taxonomy/capec-3.9/162), [20](/taxonomy/capec-3.9/20), [204](/taxonomy/capec-3.9/204), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [272](/taxonomy/capec-3.9/272), [31](/taxonomy/capec-3.9/31), [37](/taxonomy/capec-3.9/37), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [55](/taxonomy/capec-3.9/55), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## V11.2.2

Verify that the application is designed with crypto agility such that random number, authenticated encryption, MAC, or hashing algorithms, key lengths, rounds, ciphers and modes can be reconfigured, upgraded, or swapped at any time, to protect against cryptographic breaks. Similarly, it must also be possible to replace keys and passwords and re-encrypt data. This will allow for seamless upgrades to post-quantum cryptography (PQC), once high-assurance implementations of approved PQC schemes or standards are widely available.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [20](/taxonomy/capec-3.9/20), [461](/taxonomy/capec-3.9/461), [473](/taxonomy/capec-3.9/473), [97](/taxonomy/capec-3.9/97)

## V11.2.3

Verify that all cryptographic primitives utilize a minimum of 128-bits of security based on the algorithm, key size, and configuration. For example, a 256-bit ECC key provides roughly 128 bits of security where RSA requires a 3072-bit key to achieve 128 bits of security.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [272](/taxonomy/capec-3.9/272), [39](/taxonomy/capec-3.9/39), [473](/taxonomy/capec-3.9/473), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## V11.2.4

Verify that all cryptographic operations are constant-time, with no 'short-circuit' operations in comparisons, calculations, or returns, to avoid leaking information.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [272](/taxonomy/capec-3.9/272), [31](/taxonomy/capec-3.9/31), [37](/taxonomy/capec-3.9/37), [39](/taxonomy/capec-3.9/39), [463](/taxonomy/capec-3.9/463), [473](/taxonomy/capec-3.9/473), [55](/taxonomy/capec-3.9/55), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## V11.2.5

Verify that all cryptographic modules fail securely, and errors are handled in a way that does not enable vulnerabilities, such as Padding Oracle attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112), [114](/taxonomy/capec-3.9/114), [145](/taxonomy/capec-3.9/145), [157](/taxonomy/capec-3.9/157), [20](/taxonomy/capec-3.9/20), [216](/taxonomy/capec-3.9/216), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [24](/taxonomy/capec-3.9/24), [272](/taxonomy/capec-3.9/272), [31](/taxonomy/capec-3.9/31), [37](/taxonomy/capec-3.9/37), [39](/taxonomy/capec-3.9/39), [461](/taxonomy/capec-3.9/461), [463](/taxonomy/capec-3.9/463), [473](/taxonomy/capec-3.9/473), [54](/taxonomy/capec-3.9/54), [55](/taxonomy/capec-3.9/55), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [94](/taxonomy/capec-3.9/94), [97](/taxonomy/capec-3.9/97)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
