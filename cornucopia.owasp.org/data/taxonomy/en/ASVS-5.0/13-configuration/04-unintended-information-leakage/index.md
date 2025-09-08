# Unintended Information Leakage
## V13.4.1
Verify that the application is deployed either without any source control metadata, including the .git or .svn folders, or in a way that these folders are inaccessible both externally and to the application itself.
Required for Level 1, 2 and 3
## V13.4.2
Verify that debug modes are disabled for all components in production environments to prevent exposure of debugging features and information leakage.
Required for Level 2 and 3
## V13.4.3
Verify that web servers do not expose directory listings to clients unless explicitly intended.
Required for Level 2 and 3
## V13.4.4
Verify that using the HTTP TRACE method is not supported in production environments, to avoid potential information leakage.
Required for Level 2 and 3
## V13.4.5
Verify that documentation (such as for internal APIs) and monitoring endpoints are not exposed unless explicitly intended.
Required for Level 2 and 3
## V13.4.6
Verify that the application does not expose detailed version information of backend components.
Required for Level 3
## V13.4.7
Verify that the web tier is configured to only serve files with specific file extensions to prevent unintentional information, configuration, and source code leakage.
Required for Level 3
## Disclaimer
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
