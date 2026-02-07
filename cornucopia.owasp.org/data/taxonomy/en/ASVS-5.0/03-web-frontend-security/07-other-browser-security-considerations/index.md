# Other Browser Security Considerations

## V3.7.1

Verify that the application only uses client-side technologies which are still supported and considered secure. Examples of technologies which do not meet this requirement include NSAPI plugins, Flash, Shockwave, ActiveX, Silverlight, NACL, or client-side Java applets.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [181](/taxonomy/capec-3.9/181/index.md), [21](/taxonomy/capec-3.9/21/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md)

## V3.7.2

Verify that the application will only automatically redirect the user to a different hostname or domain (which is not controlled by the application) where the destination appears on an allowlist.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [173](/taxonomy/capec-3.9/173/index.md), [21](/taxonomy/capec-3.9/21/index.md), [242](/taxonomy/capec-3.9/242/index.md), [569](/taxonomy/capec-3.9/569/index.md)

## V3.7.3

Verify that the application shows a notification when the user is being redirected to a URL outside of the application's control, with an option to cancel the navigation.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [173](/taxonomy/capec-3.9/173/index.md), [21](/taxonomy/capec-3.9/21/index.md), [242](/taxonomy/capec-3.9/242/index.md), [569](/taxonomy/capec-3.9/569/index.md), [62](/taxonomy/capec-3.9/62/index.md)

## V3.7.4

Verify that the application's top-level domain (e.g., site.tld) is added to the public preload list for HTTP Strict Transport Security (HSTS). This ensures that the use of TLS for the application is built directly into the main browsers, rather than relying only on the Strict-Transport-Security response header field.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [157](/taxonomy/capec-3.9/157/index.md), [21](/taxonomy/capec-3.9/21/index.md), [220](/taxonomy/capec-3.9/220/index.md), [242](/taxonomy/capec-3.9/242/index.md), [31](/taxonomy/capec-3.9/31/index.md), [39](/taxonomy/capec-3.9/39/index.md), [466](/taxonomy/capec-3.9/466/index.md), [569](/taxonomy/capec-3.9/569/index.md), [593](/taxonomy/capec-3.9/593/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [89](/taxonomy/capec-3.9/89/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V3.7.5

Verify that the application behaves as documented (such as warning the user or blocking access) if the browser used to access the application does not support the expected security features.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [103](/taxonomy/capec-3.9/103/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [176](/taxonomy/capec-3.9/176/index.md), [19](/taxonomy/capec-3.9/19/index.md), [202](/taxonomy/capec-3.9/202/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [242](/taxonomy/capec-3.9/242/index.md), [554](/taxonomy/capec-3.9/554/index.md), [63](/taxonomy/capec-3.9/63/index.md), [87](/taxonomy/capec-3.9/87/index.md), [89](/taxonomy/capec-3.9/89/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
