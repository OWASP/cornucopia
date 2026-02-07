# HTTP Message Structure Validation

## V4.2.1

Verify that all application components (including load balancers, firewalls, and application servers) determine boundaries of incoming HTTP messages using the appropriate mechanism for the HTTP version to prevent HTTP request smuggling. In HTTP/1.x, if a Transfer-Encoding header field is present, the Content-Length header must be ignored per RFC 2616. When using HTTP/2 or HTTP/3, if a Content-Length header field is present, the receiver must ensure that it is consistent with the length of the DATA frames.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [105](/taxonomy/capec-3.9/105/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [33](/taxonomy/capec-3.9/33/index.md)

## V4.2.2

Verify that when generating HTTP messages, the Content-Length header field does not conflict with the length of the content as determined by the framing of the HTTP protocol, in order to prevent request smuggling attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [105](/taxonomy/capec-3.9/105/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [33](/taxonomy/capec-3.9/33/index.md)

## V4.2.3

Verify that the application does not send nor accept HTTP/2 or HTTP/3 messages with connection-specific header fields such as Transfer-Encoding to prevent response splitting and header injection attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [105](/taxonomy/capec-3.9/105/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [33](/taxonomy/capec-3.9/33/index.md)

## V4.2.4

Verify that the application only accepts HTTP/2 and HTTP/3 requests where the header fields and values do not contain any CR (\r), LF (\n), or CRLF (\r\n) sequences, to prevent header injection attacks.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [105](/taxonomy/capec-3.9/105/index.md), [220](/taxonomy/capec-3.9/220/index.md), [272](/taxonomy/capec-3.9/272/index.md), [28](/taxonomy/capec-3.9/28/index.md), [33](/taxonomy/capec-3.9/33/index.md)

## V4.2.5

Verify that, if the application (backend or frontend) builds and sends requests, it uses validation, sanitization, or other mechanisms to avoid creating URIs (such as for API calls) or HTTP request header fields (such as Authorization or Cookie), which are too long to be accepted by the receiving component. This could cause a denial of service, such as when sending an overly long request (e.g., a long cookie header field), which results in the server always responding with an error status.

Required for Level 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [100](/taxonomy/capec-3.9/100/index.md), [227](/taxonomy/capec-3.9/227/index.md), [25](/taxonomy/capec-3.9/25/index.md), [28](/taxonomy/capec-3.9/28/index.md)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
