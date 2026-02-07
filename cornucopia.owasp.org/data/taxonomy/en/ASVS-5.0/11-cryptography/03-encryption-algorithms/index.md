# Encryption Algorithms

## V11.3.1

Verify that insecure block modes (e.g., ECB) and weak padding schemes (e.g., PKCS#1 v1.5) are not used.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [20](/taxonomy/capec-3.9/20/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [39](/taxonomy/capec-3.9/39/index.md), [461](/taxonomy/capec-3.9/461/index.md), [463](/taxonomy/capec-3.9/463/index.md), [473](/taxonomy/capec-3.9/473/index.md), [55](/taxonomy/capec-3.9/55/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## V11.3.2

Verify that only approved ciphers and modes such as AES with GCM are used.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [162](/taxonomy/capec-3.9/162/index.md), [20](/taxonomy/capec-3.9/20/index.md), [204](/taxonomy/capec-3.9/204/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [39](/taxonomy/capec-3.9/39/index.md), [461](/taxonomy/capec-3.9/461/index.md), [473](/taxonomy/capec-3.9/473/index.md), [55](/taxonomy/capec-3.9/55/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## V11.3.3

Verify that encrypted data is protected against unauthorized modification preferably by using an approved authenticated encryption method or by combining an approved encryption method with an approved MAC algorithm.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [162](/taxonomy/capec-3.9/162/index.md), [184](/taxonomy/capec-3.9/184/index.md), [20](/taxonomy/capec-3.9/20/index.md), [204](/taxonomy/capec-3.9/204/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [39](/taxonomy/capec-3.9/39/index.md), [438](/taxonomy/capec-3.9/438/index.md), [442](/taxonomy/capec-3.9/442/index.md), [461](/taxonomy/capec-3.9/461/index.md), [473](/taxonomy/capec-3.9/473/index.md), [475](/taxonomy/capec-3.9/475/index.md), [523](/taxonomy/capec-3.9/523/index.md), [55](/taxonomy/capec-3.9/55/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [68](/taxonomy/capec-3.9/68/index.md), [690](/taxonomy/capec-3.9/690/index.md), [75](/taxonomy/capec-3.9/75/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## V11.3.4

Verify that nonces, initialization vectors, and other single-use numbers are not used for more than one encryption key and data-element pair. The method of generation must be appropriate for the algorithm being used.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [20](/taxonomy/capec-3.9/20/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [39](/taxonomy/capec-3.9/39/index.md), [473](/taxonomy/capec-3.9/473/index.md), [55](/taxonomy/capec-3.9/55/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## V11.3.5

Verify that any combination of an encryption algorithm and a MAC algorithm is operating in encrypt-then-MAC mode.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [112](/taxonomy/capec-3.9/112/index.md), [114](/taxonomy/capec-3.9/114/index.md), [145](/taxonomy/capec-3.9/145/index.md), [157](/taxonomy/capec-3.9/157/index.md), [20](/taxonomy/capec-3.9/20/index.md), [216](/taxonomy/capec-3.9/216/index.md), [218](/taxonomy/capec-3.9/218/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [31](/taxonomy/capec-3.9/31/index.md), [37](/taxonomy/capec-3.9/37/index.md), [39](/taxonomy/capec-3.9/39/index.md), [461](/taxonomy/capec-3.9/461/index.md), [473](/taxonomy/capec-3.9/473/index.md), [475](/taxonomy/capec-3.9/475/index.md), [55](/taxonomy/capec-3.9/55/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [94](/taxonomy/capec-3.9/94/index.md), [97](/taxonomy/capec-3.9/97/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
