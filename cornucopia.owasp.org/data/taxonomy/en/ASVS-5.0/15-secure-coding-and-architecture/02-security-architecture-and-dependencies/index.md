#  Security Architecture and Dependencies
## V15.2.1
Verify that the application only contains components which have not breached the documented update and remediation time frames.
Required for Level 1, 2 and 3
## V15.2.2
Verify that the application has implemented defenses against loss of availability due to functionality which is time-consuming or resource-demanding, based on the documented security decisions and strategies for this.
Required for Level 2 and 3
## V15.2.3
Verify that the production environment only includes functionality that is required for the application to function, and does not expose extraneous functionality such as test code, sample snippets, and development functionality.
Required for Level 2 and 3
## V15.2.4
Verify that third-party components and all of their transitive dependencies are included from the expected repository, whether internally owned or an external source, and that there is no risk of a dependency confusion attack.
Required for Level 3
## V15.2.5
Verify that the application implements additional protections around parts of the application which are documented as containing "dangerous functionality" or using third-party libraries considered to be "risky components". This could include techniques such as sandboxing, encapsulation, containerization or network level isolation to delay and deter attackers who compromise one part of an application from pivoting elsewhere in the application.
Required for Level 3

## Disclaimer:
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
