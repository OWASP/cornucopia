# Secure Coding and Architecture Documentation
## V15.1.1
Verify that application documentation defines risk based remediation time frames for 3rd party component versions with vulnerabilities and for updating libraries in general, to minimize the risk from these components.
Required for Level 1, 2 and 3
## V15.1.2
Verify that an inventory catalog, such as software bill of materials (SBOM), is maintained of all third-party libraries in use, including verifying that components come from pre-defined, trusted, and continually maintained repositories.
Required for Level 2 and 3
## V15.1.3
Verify that the application documentation identifies functionality which is time-consuming or resource-demanding. This must include how to prevent a loss of availability due to overusing this functionality and how to avoid a situation where building a response takes longer than the consumer's timeout. Potential defenses may include asynchronous processing, using queues, and limiting parallel processes per user and per application.
Required for Level 2 and 3
## V15.1.4
Verify that application documentation highlights third-party libraries which are considered to be "risky components".
Required for Level 3
## V15.1.5
Verify that application documentation highlights parts of the application where "dangerous functionality" is being used.
Required for Level 3
## Disclaimer
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
