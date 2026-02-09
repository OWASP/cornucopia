# Browser Origin Separation

## V3.5.1

Verify that, if the application does not rely on the CORS preflight mechanism to prevent disallowed cross-origin requests to use sensitive functionality, these requests are validated to ensure they originate from the application itself. This may be done by using and validating anti-forgery tokens or requiring extra HTTP header fields that are not CORS-safelisted request-header fields. This is to defend against browser-based request forgery attacks, commonly known as cross-site request forgery (CSRF).

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [173](/taxonomy/capec-3.9/173/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [62](/taxonomy/capec-3.9/62/index.md)

## V3.5.2

Verify that, if the application relies on the CORS preflight mechanism to prevent disallowed cross-origin use of sensitive functionality, it is not possible to call the functionality with a request which does not trigger a CORS-preflight request. This may require checking the values of the 'Origin' and 'Content-Type' request header fields or using an extra header field that is not a CORS-safelisted header-field.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [173](/taxonomy/capec-3.9/173/index.md), [233](/taxonomy/capec-3.9/233/index.md), [62](/taxonomy/capec-3.9/62/index.md)

## V3.5.3

Verify that HTTP requests to sensitive functionality use appropriate HTTP methods such as POST, PUT, PATCH, or DELETE, and not methods defined by the HTTP specification as "safe" such as HEAD, OPTIONS, or GET. Alternatively, strict validation of the Sec-Fetch-* request header fields can be used to ensure that the request did not originate from an inappropriate cross-origin call, a navigation request, or a resource load (such as an image source) where this is not expected.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [173](/taxonomy/capec-3.9/173/index.md), [233](/taxonomy/capec-3.9/233/index.md), [446](/taxonomy/capec-3.9/446/index.md), [62](/taxonomy/capec-3.9/62/index.md)

## V3.5.4

Verify that separate applications are hosted on different hostnames to leverage the restrictions provided by same-origin policy, including how documents or scripts loaded by one origin can interact with resources from another origin and hostname-based restrictions on cookies.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [19](/taxonomy/capec-3.9/19/index.md), [21](/taxonomy/capec-3.9/21/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [31](/taxonomy/capec-3.9/31/index.md), [446](/taxonomy/capec-3.9/446/index.md), [61](/taxonomy/capec-3.9/61/index.md), [62](/taxonomy/capec-3.9/62/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## V3.5.5

Verify that messages received by the postMessage interface are discarded if the origin of the message is not trusted, or if the syntax of the message is invalid.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md), [62](/taxonomy/capec-3.9/62/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## V3.5.6

Verify that JSONP functionality is not enabled anywhere across the application to avoid Cross-Site Script Inclusion (XSSI) attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [19](/taxonomy/capec-3.9/19/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md), [62](/taxonomy/capec-3.9/62/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## V3.5.7

Verify that data requiring authorization is not included in script resource responses, like JavaScript files, to prevent Cross-Site Script Inclusion (XSSI) attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [207](/taxonomy/capec-3.9/207/index.md), [212](/taxonomy/capec-3.9/212/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md), [62](/taxonomy/capec-3.9/62/index.md), [63](/taxonomy/capec-3.9/63/index.md), [74](/taxonomy/capec-3.9/74/index.md), [77](/taxonomy/capec-3.9/77/index.md)

## V3.5.8

Verify that authenticated resources (such as images, videos, scripts, and other documents) can be loaded or embedded on behalf of the user only when intended. This can be accomplished by strict validation of the Sec-Fetch-* HTTP request header fields to ensure that the request did not originate from an inappropriate cross-origin call, or by setting a restrictive Cross-Origin-Resource-Policy HTTP response header field to instruct the browser to block returned content.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [233](/taxonomy/capec-3.9/233/index.md), [569](/taxonomy/capec-3.9/569/index.md), [62](/taxonomy/capec-3.9/62/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
