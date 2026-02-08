# Browser Security Mechanism Headers

## V3.4.1

Verify that a Strict-Transport-Security header field is included on all responses to enforce an HTTP Strict Transport Security (HSTS) policy. A maximum age of at least 1 year must be defined, and for L2 and up, the policy must apply to all subdomains as well.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [157](/taxonomy/capec-3.9/157/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [220](/taxonomy/capec-3.9/220/index.md), [31](/taxonomy/capec-3.9/31/index.md), [39](/taxonomy/capec-3.9/39/index.md), [466](/taxonomy/capec-3.9/466/index.md), [593](/taxonomy/capec-3.9/593/index.md), [594](/taxonomy/capec-3.9/594/index.md), [620](/taxonomy/capec-3.9/620/index.md), [89](/taxonomy/capec-3.9/89/index.md), [94](/taxonomy/capec-3.9/94/index.md)

## V3.4.2

Verify that the Cross-Origin Resource Sharing (CORS) Access-Control-Allow-Origin header field is a fixed value by the application, or if the Origin HTTP request header field value is used, it is validated against an allowlist of trusted origins. When 'Access-Control-Allow-Origin: *' needs to be used, verify that the response does not include any sensitive information.

Required for Level 1, 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [173](/taxonomy/capec-3.9/173/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [233](/taxonomy/capec-3.9/233/index.md), [466](/taxonomy/capec-3.9/466/index.md)

## V3.4.3

Verify that HTTP responses include a Content-Security-Policy response header field which defines directives to ensure the browser only loads and executes trusted content or resources, in order to limit execution of malicious JavaScript. As a minimum, a global policy must be used which includes the directives object-src 'none' and base-uri 'none' and defines either an allowlist or uses nonces or hashes. For an L3 application, a per-response policy with nonces or hashes must be defined.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [103](/taxonomy/capec-3.9/103/index.md), [104](/taxonomy/capec-3.9/104/index.md), [111](/taxonomy/capec-3.9/111/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md), [63](/taxonomy/capec-3.9/63/index.md), [89](/taxonomy/capec-3.9/89/index.md)

## V3.4.4

Verify that all HTTP responses contain an 'X-Content-Type-Options: nosniff' header field. This instructs browsers not to use content sniffing and MIME type guessing for the given response, and to require the response's Content-Type header field value to match the destination resource. For example, the response to a request for a style is only accepted if the response's Content-Type is 'text/css'. This also enables the use of the Cross-Origin Read Blocking (CORB) functionality by the browser.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [152](/taxonomy/capec-3.9/152/index.md), [19](/taxonomy/capec-3.9/19/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [569](/taxonomy/capec-3.9/569/index.md), [63](/taxonomy/capec-3.9/63/index.md), [690](/taxonomy/capec-3.9/690/index.md)

## V3.4.5

Verify that the application sets a referrer policy to prevent leakage of technically sensitive data to third-party services via the 'Referer' HTTP request header field. This can be done using the Referrer-Policy HTTP response header field or via HTML element attributes. Sensitive data could include path and query data in the URL, and for internal non-public applications also the hostname.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [22](/taxonomy/capec-3.9/22/index.md), [569](/taxonomy/capec-3.9/569/index.md)

## V3.4.6

Verify that the web application uses the frame-ancestors directive of the Content-Security-Policy header field for every HTTP response to ensure that it cannot be embedded by default and that embedding of specific resources is allowed only when necessary. Note that the X-Frame-Options header field, although supported by browsers, is obsolete and may not be relied upon.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [103](/taxonomy/capec-3.9/103/index.md), [104](/taxonomy/capec-3.9/104/index.md), [111](/taxonomy/capec-3.9/111/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## V3.4.7

Verify that the Content-Security-Policy header field specifies a location to report violations.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [103](/taxonomy/capec-3.9/103/index.md), [104](/taxonomy/capec-3.9/104/index.md), [111](/taxonomy/capec-3.9/111/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [207](/taxonomy/capec-3.9/207/index.md), [21](/taxonomy/capec-3.9/21/index.md), [22](/taxonomy/capec-3.9/22/index.md), [233](/taxonomy/capec-3.9/233/index.md), [242](/taxonomy/capec-3.9/242/index.md), [446](/taxonomy/capec-3.9/446/index.md), [63](/taxonomy/capec-3.9/63/index.md), [89](/taxonomy/capec-3.9/89/index.md)

## V3.4.8

Verify that all HTTP responses that initiate a document rendering (such as responses with Content-Type text/html), include the CrossOriginOpenerPolicy header field with the same-origin directive or the same-origin-allow-popups directive as required. This prevents attacks that abuse shared access to Window objects, such as tabnabbing and frame counting.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [104](/taxonomy/capec-3.9/104/index.md), [152](/taxonomy/capec-3.9/152/index.md), [160](/taxonomy/capec-3.9/160/index.md), [173](/taxonomy/capec-3.9/173/index.md), [19](/taxonomy/capec-3.9/19/index.md), [233](/taxonomy/capec-3.9/233/index.md), [466](/taxonomy/capec-3.9/466/index.md), [543](/taxonomy/capec-3.9/543/index.md), [569](/taxonomy/capec-3.9/569/index.md), [63](/taxonomy/capec-3.9/63/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
