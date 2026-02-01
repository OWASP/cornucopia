# Encryption Algorithms
## V11.3.1
Verify that insecure block modes (e.g., ECB) and weak padding schemes (e.g., PKCS#1 v1.5) are not used.
Required for Level 1, 2 and 3
## V11.3.2
Verify that only approved ciphers and modes such as AES with GCM are used.
Required for Level 1, 2 and 3
## V11.3.3
Verify that encrypted data is protected against unauthorized modification preferably by using an approved authenticated encryption method or by combining an approved encryption method with an approved MAC algorithm.
Required for Level 2 and 3
## V11.3.4
Verify that nonces, initialization vectors, and other single-use numbers are not used for more than one encryption key and data-element pair. The method of generation must be appropriate for the algorithm being used.
Required for Level 3
## V11.3.5
Verify that any combination of an encryption algorithm and a MAC algorithm is operating in encrypt-then-MAC mode.
Required for Level 3
## Disclaimer
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
