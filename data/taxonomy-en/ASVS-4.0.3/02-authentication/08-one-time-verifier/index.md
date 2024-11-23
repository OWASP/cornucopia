#  One Time Verifier
## V2.8.1
Verify that time-based OTPs have a defined lifetime before expiring.
Level 1 required: True
Level 2 required: True
Level 3 required: True
CWE: [613](https://cwe.mitre.org/data/definitions/613)
## V2.8.2
Verify that symmetric keys used to verify submitted OTPs are highly protected, such as by using a hardware security module or secure operating system based key storage.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [320](https://cwe.mitre.org/data/definitions/320)
## V2.8.3
Verify that approved cryptographic algorithms are used in the generation, seeding, and verification of OTPs.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [326](https://cwe.mitre.org/data/definitions/326)
## V2.8.4
Verify that time-based OTP can be used only once within the validity period.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [287](https://cwe.mitre.org/data/definitions/287)
## V2.8.5
Verify that if a time-based multi-factor OTP token is re-used during the validity period, it is logged and rejected with secure notifications being sent to the holder of the device.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [287](https://cwe.mitre.org/data/definitions/287)
## V2.8.6
Verify physical single-factor OTP generator can be revoked in case of theft or other loss. Ensure that revocation is immediately effective across logged in sessions, regardless of location.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [613](https://cwe.mitre.org/data/definitions/613)
## V2.8.7
Verify that biometric authenticators are limited to use only as secondary factors in conjunction with either something you have and something you know.
Level 1 required: False
Level 2 required: True
Level 3 required: True
CWE: [308](https://cwe.mitre.org/data/definitions/308)

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/). For more information visit [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.
