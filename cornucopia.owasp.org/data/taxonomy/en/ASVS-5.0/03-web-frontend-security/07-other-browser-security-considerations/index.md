# Other Browser Security Considerations

## V3.7.1

Verify that the application only uses client-side technologies which are still supported and considered secure. Examples of technologies which do not meet this requirement include NSAPI plugins, Flash, Shockwave, ActiveX, Silverlight, NACL, or client-side Java applets.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [181](/taxonomy/capec-3.9/181), [21](/taxonomy/capec-3.9/21), [242](/taxonomy/capec-3.9/242), [446](/taxonomy/capec-3.9/446)

## V3.7.2

Verify that the application will only automatically redirect the user to a different hostname or domain (which is not controlled by the application) where the destination appears on an allowlist.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [173](/taxonomy/capec-3.9/173), [21](/taxonomy/capec-3.9/21), [242](/taxonomy/capec-3.9/242), [569](/taxonomy/capec-3.9/569)

## V3.7.3

Verify that the application shows a notification when the user is being redirected to a URL outside of the application's control, with an option to cancel the navigation.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [173](/taxonomy/capec-3.9/173), [21](/taxonomy/capec-3.9/21), [242](/taxonomy/capec-3.9/242), [569](/taxonomy/capec-3.9/569), [62](/taxonomy/capec-3.9/62)

## V3.7.4

Verify that the application's top-level domain (e.g., site.tld) is added to the public preload list for HTTP Strict Transport Security (HSTS). This ensures that the use of TLS for the application is built directly into the main browsers, rather than relying only on the Strict-Transport-Security response header field.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [157](/taxonomy/capec-3.9/157), [21](/taxonomy/capec-3.9/21), [220](/taxonomy/capec-3.9/220), [242](/taxonomy/capec-3.9/242), [31](/taxonomy/capec-3.9/31), [39](/taxonomy/capec-3.9/39), [466](/taxonomy/capec-3.9/466), [569](/taxonomy/capec-3.9/569), [593](/taxonomy/capec-3.9/593), [594](/taxonomy/capec-3.9/594), [620](/taxonomy/capec-3.9/620), [89](/taxonomy/capec-3.9/89), [94](/taxonomy/capec-3.9/94)

## V3.7.5

Verify that the application behaves as documented (such as warning the user or blocking access) if the browser used to access the application does not support the expected security features.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [103](/taxonomy/capec-3.9/103), [152](/taxonomy/capec-3.9/152), [160](/taxonomy/capec-3.9/160), [176](/taxonomy/capec-3.9/176), [19](/taxonomy/capec-3.9/19), [202](/taxonomy/capec-3.9/202), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [242](/taxonomy/capec-3.9/242), [554](/taxonomy/capec-3.9/554), [63](/taxonomy/capec-3.9/63), [87](/taxonomy/capec-3.9/87), [89](/taxonomy/capec-3.9/89)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
