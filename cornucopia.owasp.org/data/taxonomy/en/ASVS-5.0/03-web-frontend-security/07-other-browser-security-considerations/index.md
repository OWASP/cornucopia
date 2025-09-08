# Other Browser Security Considerations
## V3.7.1
Verify that the application only uses client-side technologies which are still supported and considered secure. Examples of technologies which do not meet this requirement include NSAPI plugins, Flash, Shockwave, ActiveX, Silverlight, NACL, or client-side Java applets.
Required for Level 2 and 3
## V3.7.2
Verify that the application will only automatically redirect the user to a different hostname or domain (which is not controlled by the application) where the destination appears on an allowlist.
Required for Level 2 and 3
## V3.7.3
Verify that the application shows a notification when the user is being redirected to a URL outside of the application's control, with an option to cancel the navigation.
Required for Level 3
## V3.7.4
Verify that the application's top-level domain (e.g., site.tld) is added to the public preload list for HTTP Strict Transport Security (HSTS). This ensures that the use of TLS for the application is built directly into the main browsers, rather than relying only on the Strict-Transport-Security response header field.
Required for Level 3
## V3.7.5
Verify that the application behaves as documented (such as warning the user or blocking access) if the browser used to access the application does not support the expected security features.
Required for Level 3
## Disclaimer
Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
